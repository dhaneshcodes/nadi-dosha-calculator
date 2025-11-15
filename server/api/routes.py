"""
API routes/endpoints
"""
from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import Response
from server.api.schemas import (
    CalculationRequest, CalculationResponse, ErrorResponse,
    NadiCalculationRequest, NadiComparisonResult, PersonNadiResult
)
from server.domain.models import BirthDetails
from server.services.nadi_calculation_service import NadiCalculationService
from server.services.geocoding_service import geocoding_service
from server.services.timezone_service import timezone_service
from server.utils.logger import setup_logger
from typing import Optional

router = APIRouter(prefix="/api", tags=["calculations"])

# Initialize logger
logger = setup_logger("api")

# Initialize service (follows DIP - can be injected for testing)
calculation_service = NadiCalculationService()


@router.post(
    "/calculate-nadi",
    response_model=CalculationResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        500: {"model": ErrorResponse, "description": "Calculation error"}
    },
    summary="Calculate Nadi Dosha",
    description="""
    Calculate Nakshatra, Pada, and Nadi type from birth details.
    
    Uses enhanced astronomical calculations:
    - IAU 2000B lunar elements
    - 60 ELP2000-85 periodic terms
    - Lahiri Ayanamsa with nutation correction
    - Accuracy: ±0.5 arc-minutes
    """
)
async def calculate_nadi(request: CalculationRequest) -> CalculationResponse:
    """
    Calculate Nadi from birth details.
    
    Args:
        request: Calculation request with birth details
        
    Returns:
        Calculation result with Nakshatra, Pada, and Nadi
    """
    try:
        logger.info(
            f"Calculation request: date={request.birth_date}, "
            f"time={request.birth_time}, timezone={request.timezone}"
        )
        
        # Convert request to domain model
        birth_details = BirthDetails(
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            timezone=request.timezone,
            latitude=request.latitude,
            longitude=request.longitude
        )
        
        # Perform calculation
        result = calculation_service.calculate(birth_details)
        
        if result is None:
            logger.warning(f"Calculation returned None for: {request.birth_date}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to calculate Nadi. Please check your input values."
            )
        
        logger.info(
            f"Calculation successful: nakshatra={result.nakshatra}, "
            f"nadi={result.nadi}, pada={result.pada}"
        )
        
        # Convert to response model
        return CalculationResponse(**result.to_dict())
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Log full error with traceback
        logger.error(f"Unexpected calculation error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during calculation. Please try again."
        )


@router.post(
    "/calculate-nadi-complete",
    response_model=NadiComparisonResult,
    status_code=status.HTTP_200_OK,
    summary="Complete Nadi Calculation",
    description="""
    Complete Nadi Dosha calculation workflow - all logic on server side.
    
    Client sends:
    - Person name, birth date, birth time, place of birth
    
    Server handles:
    - Geocoding (database-first, then APIs)
    - Timezone detection
    - Astronomical calculations
    - Nadi determination
    
    Returns:
    - Complete result with Nadi types and compatibility analysis
    """
)
async def calculate_nadi_complete(request: NadiCalculationRequest) -> NadiComparisonResult:
    """
    Complete Nadi calculation - single API call handles everything.
    
    This endpoint handles the entire workflow:
    1. Geocode place of birth
    2. Get timezone
    3. Calculate Nadi
    4. Compare (if two persons)
    5. Return complete result
    """
    try:
        logger.info(f"Complete calculation request: person1={request.person1.name}, person2={request.person2.name if request.person2 else None}")
        
        # Process Person 1
        logger.info(f"Processing Person 1: {request.person1.place_of_birth}")
        
        # Step 1: Geocode
        geo1 = await geocoding_service.geocode(request.person1.place_of_birth)
        logger.info(f"Person 1 geocoded: {geo1['lat']}, {geo1['lon']} (source: {geo1['source']})")
        
        # Step 2: Get timezone
        tz_offset1 = await timezone_service.get_timezone(geo1['lat'], geo1['lon'], geo1)
        logger.info(f"Person 1 timezone offset: {tz_offset1} hours")
        
        # Step 3: Calculate Nadi
        from server.domain.models import BirthDetails
        birth_details1 = BirthDetails(
            birth_date=request.person1.birth_date,
            birth_time=request.person1.birth_time,
            timezone=str(tz_offset1),
            latitude=geo1['lat'],
            longitude=geo1['lon']
        )
        
        result1 = calculation_service.calculate(birth_details1)
        if not result1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to calculate Nadi for person 1"
            )
        
        person1_result = PersonNadiResult(
            name=request.person1.name,
            **result1.to_dict()
        )
        
        # Process Person 2 if provided
        person2_result = None
        has_dosha = False
        dosha_type = None
        compatible = True
        message = ""
        
        if request.person2:
            logger.info(f"Processing Person 2: {request.person2.place_of_birth}")
            
            # Geocode Person 2
            geo2 = await geocoding_service.geocode(request.person2.place_of_birth)
            logger.info(f"Person 2 geocoded: {geo2['lat']}, {geo2['lon']} (source: {geo2['source']})")
            
            # Get timezone Person 2
            tz_offset2 = await timezone_service.get_timezone(geo2['lat'], geo2['lon'], geo2)
            logger.info(f"Person 2 timezone offset: {tz_offset2} hours")
            
            # Calculate Nadi Person 2
            birth_details2 = BirthDetails(
                birth_date=request.person2.birth_date,
                birth_time=request.person2.birth_time,
                timezone=str(tz_offset2),
                latitude=geo2['lat'],
                longitude=geo2['lon']
            )
            
            result2 = calculation_service.calculate(birth_details2)
            if not result2:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to calculate Nadi for person 2"
                )
            
            person2_result = PersonNadiResult(
                name=request.person2.name,
                **result2.to_dict()
            )
            
            # Check for Nadi Dosha
            has_dosha = result1.nadi == result2.nadi
            compatible = not has_dosha
            
            if has_dosha:
                dosha_type = result1.nadi
                message = f"Nadi Dosha present! Both have {result1.nadi} Nadi. This combination is not recommended for marriage."
            else:
                message = f"No Nadi Dosha. {result1.nadi} and {result2.nadi} Nadis are compatible."
        else:
            # Single person mode
            message = f"{person1_result.name or 'Person'} has {result1.nadi} Nadi ({person1_result.nakshatra} Nakshatra, Pada {person1_result.pada})."
        
        logger.info(f"Calculation complete: dosha={has_dosha}, compatible={compatible}")
        
        return NadiComparisonResult(
            person1=person1_result,
            person2=person2_result,
            hasDosha=has_dosha,
            doshaType=dosha_type,
            compatible=compatible,
            message=message
        )
        
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        error_msg = str(e) if str(e) else repr(e)
        error_type = type(e).__name__
        logger.error(f"Unexpected error [{error_type}]: {error_msg}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {error_type}: {error_msg}"
        )


@router.options("/calculate-nadi-complete")
async def options_calculate_nadi_complete(request: Request):
    """Handle CORS preflight for calculate-nadi-complete endpoint"""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Max-Age": "3600",
        }
    )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Nadi Dosha Calculator API"}


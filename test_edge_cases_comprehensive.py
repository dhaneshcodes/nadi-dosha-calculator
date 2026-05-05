#!/usr/bin/env python3
"""
Comprehensive Edge Case Testing for DateTime Conversion Fix
Tests all scenarios where the bug could potentially occur
"""
import requests
import json
from datetime import datetime, timedelta
from typing import List, Tuple

API_URL = 'http://159.89.161.170:8000/api/calculate-nadi-complete'

class TestCase:
    def __init__(self, name: str, date: str, time: str, pob: str, expected_status: int = 200, description: str = ""):
        self.name = name
        self.date = date
        self.time = time
        self.pob = pob
        self.expected_status = expected_status
        self.description = description
    
    def to_dict(self):
        return {
            "person1": {
                "name": self.name,
                "birth_date": self.date,
                "birth_time": self.time,
                "place_of_birth": self.pob
            }
        }

# Test Categories
test_cases = []

# ============================================================================
# CATEGORY 1: Original Bug - 1st of Month + Early Morning Times
# ============================================================================
test_cases.extend([
    TestCase("Amar", "2025-08-01", "04:00", "Azamgarh", 200, 
             "Original failing case: 1st Aug + 4 AM IST"),
    TestCase("Test1", "2025-01-01", "04:00", "Mumbai", 200,
             "1st Jan + 4 AM (New Year + early morning)"),
    TestCase("Test2", "2025-02-01", "04:00", "Delhi", 200,
             "1st Feb + 4 AM"),
    TestCase("Test3", "2025-03-01", "04:00", "Bangalore", 200,
             "1st Mar + 4 AM"),
    TestCase("Test4", "2025-04-01", "04:00", "Chennai", 200,
             "1st Apr + 4 AM"),
    TestCase("Test5", "2025-05-01", "04:00", "Hyderabad", 200,
             "1st May + 4 AM"),
    TestCase("Test6", "2025-06-01", "04:00", "Kolkata", 200,
             "1st Jun + 4 AM"),
    TestCase("Test7", "2025-07-01", "04:00", "Pune", 200,
             "1st Jul + 4 AM"),
    TestCase("Test8", "2025-09-01", "04:00", "Ahmedabad", 200,
             "1st Sep + 4 AM"),
    TestCase("Test9", "2025-10-01", "04:00", "Jaipur", 200,
             "1st Oct + 4 AM"),
    TestCase("Test10", "2025-11-01", "04:00", "Lucknow", 200,
             "1st Nov + 4 AM"),
    TestCase("Test11", "2025-12-01", "04:00", "Kanpur", 200,
             "1st Dec + 4 AM"),
])

# ============================================================================
# CATEGORY 2: 1st of Month + Boundary Times
# ============================================================================
test_cases.extend([
    TestCase("Boundary1", "2025-08-01", "05:30", "Mumbai", 200,
             "1st Aug + 5:30 AM (exactly on timezone boundary)"),
    TestCase("Boundary2", "2025-08-01", "05:29", "Mumbai", 200,
             "1st Aug + 5:29 AM (just before boundary)"),
    TestCase("Boundary3", "2025-08-01", "05:31", "Mumbai", 200,
             "1st Aug + 5:31 AM (just after boundary)"),
    TestCase("Boundary4", "2025-08-01", "00:00", "Mumbai", 200,
             "1st Aug + Midnight"),
    TestCase("Boundary5", "2025-08-01", "03:00", "Mumbai", 200,
             "1st Aug + 3 AM (early morning)"),
    TestCase("Boundary6", "2025-08-01", "02:00", "Mumbai", 200,
             "1st Aug + 2 AM (very early morning)"),
    TestCase("Boundary7", "2025-08-01", "01:00", "Mumbai", 200,
             "1st Aug + 1 AM (very early morning)"),
])

# ============================================================================
# CATEGORY 3: 1st of Month + Late Times (Should Always Work)
# ============================================================================
test_cases.extend([
    TestCase("Late1", "2025-08-01", "06:00", "Mumbai", 200,
             "1st Aug + 6 AM (after boundary - no day change)"),
    TestCase("Late2", "2025-08-01", "10:00", "Mumbai", 200,
             "1st Aug + 10 AM"),
    TestCase("Late3", "2025-08-01", "12:00", "Mumbai", 200,
             "1st Aug + Noon"),
    TestCase("Late4", "2025-08-01", "15:00", "Mumbai", 200,
             "1st Aug + 3 PM"),
    TestCase("Late5", "2025-08-01", "23:59", "Mumbai", 200,
             "1st Aug + 11:59 PM"),
])

# ============================================================================
# CATEGORY 4: Other Dates + Early Morning (Should Always Work)
# ============================================================================
test_cases.extend([
    TestCase("Other1", "2025-08-05", "04:00", "Mumbai", 200,
             "5th Aug + 4 AM (not 1st, should work)"),
    TestCase("Other2", "2025-08-15", "04:00", "Mumbai", 200,
             "15th Aug + 4 AM"),
    TestCase("Other3", "2025-08-31", "04:00", "Mumbai", 200,
             "31st Aug + 4 AM (last day of month)"),
    TestCase("Other4", "2025-07-31", "04:00", "Mumbai", 200,
             "31st Jul + 4 AM (last day of month)"),
])

# ============================================================================
# CATEGORY 5: Month Boundaries - Late Times That Roll Over
# ============================================================================
test_cases.extend([
    TestCase("MonthBound1", "2025-07-31", "23:00", "Mumbai", 200,
             "31st Jul + 11 PM (late time near month boundary)"),
    TestCase("MonthBound2", "2025-08-31", "23:30", "Mumbai", 200,
             "31st Aug + 11:30 PM"),
    TestCase("MonthBound3", "2025-01-31", "22:00", "Mumbai", 200,
             "31st Jan + 10 PM"),
    TestCase("MonthBound4", "2025-03-31", "21:00", "Mumbai", 200,
             "31st Mar + 9 PM"),
])

# ============================================================================
# CATEGORY 6: Year Boundaries
# ============================================================================
test_cases.extend([
    TestCase("YearBound1", "2024-12-31", "04:00", "Mumbai", 200,
             "31st Dec 2024 + 4 AM (year boundary)"),
    TestCase("YearBound2", "2025-01-01", "04:00", "Mumbai", 200,
             "1st Jan 2025 + 4 AM (New Year + early morning)"),
    TestCase("YearBound3", "2024-12-31", "23:30", "Mumbai", 200,
             "31st Dec 2024 + 11:30 PM (crosses to next year)"),
    TestCase("YearBound4", "2026-01-01", "04:00", "Mumbai", 200,
             "1st Jan 2026 + 4 AM"),
])

# ============================================================================
# CATEGORY 7: Leap Year - February 29
# ============================================================================
test_cases.extend([
    TestCase("Leap1", "2024-02-29", "04:00", "Mumbai", 200,
             "29th Feb 2024 (leap year) + 4 AM"),
    TestCase("Leap2", "2024-02-29", "23:00", "Mumbai", 200,
             "29th Feb 2024 + 11 PM"),
    TestCase("Leap3", "2024-03-01", "04:00", "Mumbai", 200,
             "1st Mar 2024 (after leap day) + 4 AM"),
    TestCase("Leap4", "2025-02-28", "04:00", "Mumbai", 200,
             "28th Feb 2025 (non-leap year) + 4 AM"),
])

# ============================================================================
# CATEGORY 8: Edge Times (Midnight, Noon, etc.)
# ============================================================================
test_cases.extend([
    TestCase("Edge1", "2025-08-01", "00:00", "Mumbai", 200,
             "1st Aug + Midnight (00:00)"),
    TestCase("Edge2", "2025-08-01", "00:01", "Mumbai", 200,
             "1st Aug + 12:01 AM"),
    TestCase("Edge3", "2025-08-15", "12:00", "Mumbai", 200,
             "15th Aug + Noon"),
    TestCase("Edge4", "2025-08-15", "12:30", "Mumbai", 200,
             "15th Aug + 12:30 PM"),
    TestCase("Edge5", "2025-08-31", "23:59", "Mumbai", 200,
             "31st Aug + 11:59 PM"),
])

# ============================================================================
# CATEGORY 9: Different Cities (Different Timezones might behave differently)
# ============================================================================
test_cases.extend([
    TestCase("City1", "2025-08-01", "04:00", "Mumbai", 200,
             "1st Aug + 4 AM - Mumbai"),
    TestCase("City2", "2025-08-01", "04:00", "Delhi", 200,
             "1st Aug + 4 AM - Delhi"),
    TestCase("City3", "2025-08-01", "04:00", "Kolkata", 200,
             "1st Aug + 4 AM - Kolkata"),
    TestCase("City4", "2025-08-01", "04:00", "Bangalore", 200,
             "1st Aug + 4 AM - Bangalore"),
    TestCase("City5", "2025-08-01", "04:00", "Chennai", 200,
             "1st Aug + 4 AM - Chennai"),
])

# ============================================================================
# CATEGORY 10: Future Dates (Edge cases for date validation)
# ============================================================================
test_cases.extend([
    TestCase("Future1", "2030-01-01", "04:00", "Mumbai", 200,
             "1st Jan 2030 + 4 AM (future date)"),
    TestCase("Future2", "2099-08-01", "04:00", "Mumbai", 200,
             "1st Aug 2099 + 4 AM (far future)"),
])

# ============================================================================
# CATEGORY 11: Past Dates (Historical dates)
# ============================================================================
test_cases.extend([
    TestCase("Past1", "2000-01-01", "04:00", "Mumbai", 200,
             "1st Jan 2000 + 4 AM (past date)"),
    TestCase("Past2", "1950-08-01", "04:00", "Mumbai", 200,
             "1st Aug 1950 + 4 AM (old date)"),
])

# ============================================================================
# CATEGORY 12: Times That Cross Multiple Days (Extreme cases)
# ============================================================================
test_cases.extend([
    TestCase("Extreme1", "2025-08-01", "01:00", "Mumbai", 200,
             "1st Aug + 1 AM (crosses to previous day)"),
    TestCase("Extreme2", "2025-08-01", "02:30", "Mumbai", 200,
             "1st Aug + 2:30 AM"),
    TestCase("Extreme3", "2025-08-01", "03:45", "Mumbai", 200,
             "1st Aug + 3:45 AM"),
])

def run_tests():
    print("=" * 80)
    print("COMPREHENSIVE EDGE CASE TESTING - DateTime Conversion Fix")
    print("=" * 80)
    print(f"\nTotal Test Cases: {len(test_cases)}\n")
    
    results = {
        'passed': [],
        'failed': [],
        'errors': []
    }
    
    for i, test in enumerate(test_cases, 1):
        print(f"[{i}/{len(test_cases)}] Testing: {test.description}")
        print(f"         Date: {test.date}, Time: {test.time}, POB: {test.pob}")
        
        try:
            response = requests.post(
                API_URL,
                json=test.to_dict(),
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == test.expected_status:
                results['passed'].append(test)
                print(f"         ✅ PASSED (Status: {response.status_code})")
                
                # If successful, show brief result
                if response.status_code == 200:
                    try:
                        data = response.json()
                        nadi = data.get('person1', {}).get('nadi', 'N/A')
                        nakshatra = data.get('person1', {}).get('nakshatra', 'N/A')
                        print(f"         Result: {nakshatra} Nakshatra, {nadi} Nadi")
                    except:
                        pass
            else:
                results['failed'].append((test, response.status_code))
                print(f"         ❌ FAILED (Expected: {test.expected_status}, Got: {response.status_code})")
                
                try:
                    error_data = response.json()
                    detail = error_data.get('detail', 'No detail')
                    print(f"         Error: {detail}")
                except:
                    print(f"         Error: {response.text[:100]}")
                    
        except Exception as e:
            results['errors'].append((test, str(e)))
            print(f"         ❌ EXCEPTION: {e}")
        
        print()
    
    # Summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"✅ Passed: {len(results['passed'])}/{len(test_cases)}")
    print(f"❌ Failed: {len(results['failed'])}")
    print(f"💥 Errors: {len(results['errors'])}")
    print()
    
    if results['failed']:
        print("FAILED TESTS:")
        print("-" * 80)
        for test, status in results['failed']:
            print(f"  - {test.description}")
            print(f"    Expected: {test.expected_status}, Got: {status}")
            print()
    
    if results['errors']:
        print("ERRORS:")
        print("-" * 80)
        for test, error in results['errors']:
            print(f"  - {test.description}")
            print(f"    Error: {error}")
            print()
    
    success_rate = (len(results['passed']) / len(test_cases)) * 100
    print(f"Success Rate: {success_rate:.1f}%")
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    import sys
    try:
        results = run_tests()
        sys.exit(0 if len(results['failed']) == 0 and len(results['errors']) == 0 else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)


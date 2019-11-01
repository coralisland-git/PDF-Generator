bench_warrant_data = {
    "case_number": "123456",  # 123456
    "trial_call_date": "09/03/2019",  # (September 3, 2019) %m/%d/%Y
    "defendant_name": "John Doe",
    "defendant_address": "1 N Wacker, Chicago, IL 60606",
    "violations": [  # dynamically allocated section, "offense(s)" needs to be singular or plural based on how many violations
        {
            "violation_section": "11-11",
            "violation_description": "Test violation description",
        },
        {
            "violation_section": "22-22",
            "violation_description": "Test violation description 2",
        },
    ],
    "order_date": "09/31/2019",  # %m/%d/%Y
    "bond_amount": 500.00,
    "defendant_state_id_number": "000000",
    "defendant_dob": "04/01/1990",  # %m/%d/%Y
    "defendant_driver_license_number": "111111",
    "defendant_ssn": "000-00-0000",
}

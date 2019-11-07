remittance_report_data = {
    "defendant_name": "John Doe",
    "case_number": "123456",
    "order_date": "08/31/2019",  # %m/%d/%Y
    "citation_table": [  # citation table can have more than 4 entries
        {
            "citation_number": "1223253",
            "disposition": "Guilty",
            "length_of_sentence": "30 days",
            "computation_of_sentence": "Concurrent",
            "fine": 50.00,
            "community_service_hours": "24",
            "restitution": "TEST",
        },
        {
            "citation_number": "324342",
            "disposition": "Contest",
            "length_of_sentence": "60 days",
            "computation_of_sentence": "Probation",
            "fine": 100.00,
            "community_service_hours": "48",
            "restitution": "TEST 2",
        },
    ],
    "date_range_from": "08/01/2019",    # %m/%d/%Y
    "date_range_to": "08/31/2019",  # %m/%d/%Y
    "4_to_25": {
        "number_of_cases": 0,
        "amount_due_per_case": 3.00,
        "total_amount": 0.00
    },
    "25_to_50": {
        "number_of_cases": 3,
        "amount_due_per_case": 4.00,
        "total_amount": 12.00
    },
    "50_to_100": {
        "number_of_cases": 10,
        "amount_due_per_case": 5.00,
        "total_amount": 50.00
    },
    "over_100": {
        "number_of_cases": 14,
        "amount_due_per_case": "5% of each case",
        "total_amount": 175.00
    },
    "partial_payment": {
        "number_of_cases": 0,
        "total_amount": 0.00
    },
    "grand_total": {
        "number_of_cases": 27,
        "total_amount": 237.00
    },
    "order_date": "10/29/2019"  # %m/%d/%Y
}

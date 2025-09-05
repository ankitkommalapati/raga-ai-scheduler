from scheduling import duration_for_patient_type

def test_duration_logic():
    assert duration_for_patient_type("new") == 60
    assert duration_for_patient_type("returning") == 30
    assert duration_for_patient_type("anything-else") == 30
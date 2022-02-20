JOINING_FORM_TO_JOINEDNESS = {
    "isol": (False, False),
    "init": (False, True),
    "medi": (True, True),
    "fina": (True, False),
}


def slice_joining_form(joining_form: str, slice_into: int) -> list[str]:
    joinedness_to_name = {v: k for k, v in JOINING_FORM_TO_JOINEDNESS.items()}
    is_joined_before, is_joined_after = JOINING_FORM_TO_JOINEDNESS[joining_form]
    joining_forms = []
    if slice_into == 1:
        joining_forms.append(joining_form)
    elif slice_into > 1:
        for i in range(slice_into):
            if i == 0:
                joining_forms.append(joinedness_to_name[(is_joined_before, True)])
            elif i == slice_into - 1:
                joining_forms.append(joinedness_to_name[(True, is_joined_after)])
            else:
                joining_forms.append(joinedness_to_name[(True, True)])
    return joining_forms

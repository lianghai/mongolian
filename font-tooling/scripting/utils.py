from tptq.utils.otl import File

from data import Category


def make_glyph_classes(file: File, category_chain: list[str], category: Category):

    class_name = "@" + ".".join(category_chain)
    members = []

    for key, value in category.immediate_members.items():
        if value:
            sub_category_chain = category_chain[:] + [key]
            nested_class_name = "@" + ".".join(sub_category_chain)
            make_glyph_classes(file, sub_category_chain, value)
            members.append(nested_class_name)
        else:
            members.append("@" + key)

    if members:
        file.glyph_class(class_name, members)


def slice_joining_form(joining_form: str, slice_into: int) -> list[str]:
    name_to_joinedness = {
        "isol": (False, False),
        "init": (False, True),
        "medi": (True, True),
        "fina": (True, False),
    }
    joinedness_to_name = {v: k for k, v in name_to_joinedness.items()}
    is_joined_before, is_joined_after = name_to_joinedness[joining_form]
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

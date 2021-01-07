from tptqscripttools.otl import Writer

from data import Category


def make_class_definitions(writer: Writer, category_chain: list[str], category: Category):

    class_name = "@" + ".".join(category_chain)
    members = []
    if isinstance(category._members, dict):
        for sub_category, value in category._members.items():
            sub_category_chain = category_chain[:] + [sub_category]
            nested_class_name = "@" + ".".join(sub_category_chain)
            make_class_definitions(writer, sub_category_chain, value)
            members.append(nested_class_name)
    elif isinstance(category._members, list):
        members.extend("@" + i for i in category._members)

    if members:
        writer.classDefinition(class_name, members)


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

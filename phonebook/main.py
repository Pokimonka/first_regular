from pprint import pprint
import csv
import re

def move_first_last_and_sur_name(contacts):
    for row in contacts[1:]:
        fio = ', '.join(row[:3])
        f_i_o = (fio.replace(",", "")).split(' ')
        f_i_o = [f for f in f_i_o if f]
        lastname = f_i_o[0]
        firstname = f_i_o[1]
        surname = f_i_o[2] if len(f_i_o) > 2 else ''
        row[0] = lastname
        row[1] = firstname
        row[2] = surname
    return contacts


def set_unique_contacts(contacts):
    uni_contacts = {}
    for contact in contacts[1:]:
        if contact[0] + ' ' + contact[1] in uni_contacts:
            contact_to_zip1 = uni_contacts[contact[0] + ' ' + contact[1]]
            contact_to_zip2 = contact
            uni_contacts[contact[0] + ' ' + contact[1]] = [y if x == '' else x for x, y in
                                                              zip(contact_to_zip1, contact_to_zip2)]
        else:
            uni_contacts[contact[0] + ' ' + contact[1]] = contact
    return uni_contacts


def restore_order(uni_contacts, contacts):
    result = []
    for contact in uni_contacts.values():
        for default_contact in contacts[1:]:
            if contact not in result:
                if contact[0] == default_contact[0] and contact[1] == default_contact[1]:
                    result.append(contact)
    return result


def change_numbers(contacts):
    regex = r"(\+7|8)?(\s*\(?(\d{3})\)?\s*\-?(\d+)\s*\-?(\d{2})\s*\-?(\d{2})((((\s*)\()|(\s*))(доб.)\s*(\d+)\)?)?)"
    subst = "+7(\\3)\\4-\\5-\\6\\10\\11\\12\\13"
    for person in contacts:
        res = re.sub(regex, subst, person[5])
        if res:
            person[5] = res
    result_list = [contacts_list[0]] + contacts
    return result_list

def create_pretty_phonebook(contacts):
    pretty_contacts_list = move_first_last_and_sur_name(contacts)
    unique_contacts = set_unique_contacts(pretty_contacts_list)
    ordered_list = restore_order(unique_contacts, pretty_contacts_list)
    result = change_numbers(ordered_list)
    return result

if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding="utf-8") as f:
      rows = csv.reader(f, delimiter=",")
      contacts_list = list(rows)

    result_contacts_list = create_pretty_phonebook(contacts_list)

    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(result_contacts_list)














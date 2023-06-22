# skończone

class ListElement:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


def nil():
    return ListElement(None)


def cons(elem, lst):
    if not isinstance(elem, ListElement):
        add_elem = ListElement(elem)
    else:
        add_elem = elem
    if is_empty(lst):
        return add_elem
    else:
        add_elem.next = lst
        return add_elem


def first(lst):
    if lst is None:
        return None
    else:
        return lst.data


def rest(lst):
    if lst is None:
        raise Exception("List is empty!")
    else:
        return lst.next


def print_list(lst):
    if is_empty(lst):
        print(f"[]\n")
    elif length(lst) == 1:
        print(f"{first(lst)} -> None\n")
    else:
        first_elem = first(lst)
        rest_list = rest(lst)
        print(f"{first_elem} ->")
        print_list(rest_list)


def remove_end(lst):
    if is_empty(lst):
        raise Exception("List is already empty!")
    else:
        first_elem = first(lst)  # podział listy na: pierwszy element
        rest_list = rest(lst)  # i całą resztę
        if first(rest_list) is None:
            return create()
        if rest(rest_list) is None:
            rest_list = None
        else:
            rest_list = remove_end(rest_list)
        return cons(first_elem, rest_list)


def take(lst, n: int, result=ListElement()):
    if is_empty(lst):
        return lst
    elif n < 1:
        return create()
    else:
        first_elem = first(lst)
        rest_list = rest(lst)
        result = add_end(result, first_elem)
        if length(result) < n:
            if rest_list is None:
                return result
            result = take(rest_list, n, result)
        return result


def drop(lst, n: int, result=ListElement(), removed=0):
    if is_empty(lst):
        return lst

    elif length(result) == length(lst) - n:
        return create()
    else:
        if removed < n:
            removed += 1
            result = remove(lst)
            result = drop(remove(lst), n, result, removed)
        else:
            return lst
    return result


def create():
    return nil()


def destroy(lst):
    lst = create()
    return lst


def get(lst):
    if is_empty(lst):
        raise Exception("List is empty!")
    else:
        return first(lst)


def length(lst, len=0):
    if first(lst) is not None:
        len += 1
        rest_list = rest(lst)
        len_res = length(rest_list, len)
        return len_res
    else:
        return len


def is_empty(lst):
    if isinstance(lst, ListElement) or lst is None:
        if lst is None or first(lst) is None:
            return True
        else:
            return False
    else:
        raise Exception("This function works only for LinkedList type objects!")


def remove(lst):
    if is_empty(lst):
        raise Exception("List is empty!")
    else:
        return rest(lst)


def add(lst, elem):
    if not isinstance(elem, ListElement):
        elem = ListElement(elem)
    lst = cons(elem, lst)
    return lst


def add_end(lst, elem):
    if not isinstance(elem, ListElement):
        add_elem = ListElement(elem)
    else:
        add_elem = elem
    if is_empty(lst):
        return cons(add_elem, lst)
    else:
        first_elem = first(lst)
        rest_list = rest(lst)
        recreated_list = add_end(rest_list, add_elem)
        return cons(first_elem, recreated_list)


def main():
    list0 = [('AGH', 'Kraków', 1919), ('UJ', 'Kraków', 1364), ('PW', 'Warszawa', 1915), ('UW', 'Warszawa', 1915),
             ('UP', 'Poznań', 1919), ('PG', 'Gdańsk', 1945)]
    list1 = create()
    list1 = add(list1, list0[1])
    list1 = add(list1, list0[0])
    for i in range(2, len(list0)):
        list1 = add_end(list1, list0[i])
    print_list(list1)

    print("Remove:")

    print_list(remove(list1))

    print_list(remove_end(list1))

    print("Get:")
    print(get(list1))

    print("Length:")
    print(length(list1), "\n")

    print("Take:")
    list2 = take(list1, 4)
    print_list(list2)
    print_list(list1)

    print("Drop:")
    list2 = drop(list1, 4)
    print_list(list2)
    print_list(list1)

    print("Is empty i destroy:")
    print_list(list1)
    print("Is empty?", is_empty(list1), "\n")

    list1 = destroy(list1)
    print_list(list1)
    print("Is empty?", is_empty(list1))


if __name__ == '__main__':
    main()

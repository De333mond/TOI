from PrettyPrint import PrettyPrintTree


class Node:
    def __init__(self, title: str, children=None, weight=None):
        self.children = children
        self.title = title
        self.code = None
        self.weight = weight

    def __add__(self, other):
        self.children += other

    def __repr__(self):
        return self.title


def get_weights(message: str) -> dict:
    weights = {}
    for el in message:
        if el not in weights.keys():
            weights.update({el: 1})
        else:
            weights[el] += 1

    return dict(sorted(weights.items(), key=lambda x: x[1]))


def create_tree(message: str):
    weights = get_weights(message)
    res = []
    for key, value in weights.items():
        node = Node(key, weight=value)
        res.append(node)

    while len(res) > 1:
        buffer = []
        for _ in range(2):
            min_value, min_index = None, None
            for i, el in enumerate(res):
                if min_value is None or el.weight < min_value:
                    min_value = el.weight
                    min_index = i
            buffer.append(res.pop(min_index))

        parent_node = Node(
            ''.join([node.title for node in buffer]),
            children=buffer,
            weight=sum([node.weight for node in buffer])
        )
        res.append(parent_node)

    return res[0]


def print_tree_titles(node: Node):
    pt = PrettyPrintTree(
        lambda x: x.children,
        lambda x: ''.join(sorted(x.title)) + f'\nw: {x.weight}',
        lambda x: x.code[-1] if x.code else '',
    )

    pt(node)


def get_encoding_dict(node: Node):
    def set_codes(node: Node, parent: Node = None, n=0):
        if not node.children:
            node.code = str(n)
            if parent.code:
                node.code = parent.code + node.code
            encoding_dict.update({node.title: node.code})
        else:
            if parent:
                node.code = str(n)
                if parent.code:
                    node.code = parent.code + node.code
            for i, el in enumerate(node.children):
                set_codes(el, node, i)

    encoding_dict = {}
    set_codes(node)
    return encoding_dict


def encode(encoding_dict, message):
    encoding = ''
    for el in message:
        encoding += encoding_dict[el]
    return encoding


if __name__ == "__main__":
    message = "abracadabra"

    tree = create_tree(message)
    encoding_dict = get_encoding_dict(tree)
    print_tree_titles(tree)
    print('\n\n')
    print(f'{encoding_dict=}')
    encoding = encode(encoding_dict, message)
    print(f'{encoding=}, {len(encoding)=}')

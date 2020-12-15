# python3
import sys


class Node:
    def __init__(self, index, left, right):
        self.index = index
        self.left = left
        self.right = right
        # self.parent = parent
        self.link = 0
        self.next = {'A': -1, 'C': -1, 'G': -1, 'T': -1, '$': -1}

    @property
    def length(self):
        return min(self.right, current_end) - self.left

    # @property
    # def suffix(self):
    #     return text[self.left:self.right]


def build_suffix_tree(text):
    """
    Build a suffix tree of the string text and return a list
    with all of the labels of its edges (the corresponding
    substrings of the text) in any order.
    """
    global current_end
    current_end = -1

    len_text = len(text)
    # suffix_tree: List[Node] = [Node(-1, -1, -1, -1)] * (len_text * 2 + 2)
    suffix_tree = [Node(-1, -1, -1)] * (len_text * 2 + 2)
    node_count = 1
    # suffix_tree[0] = Node(0, -1, len_text, -1)
    suffix_tree[0] = Node(0, -1, -1)
    root = suffix_tree[0]

    # active point
    active_node = root
    active_edge_index = -1
    active_edge_char = ''
    active_length = 0
    # active point

    remainder = 0

    for i in range(len_text):
        current_end = i + 1
        char_to_insert = text[i]
        remainder += 1
        if remainder == 1:
            active_edge_index = i
            active_edge_char = char_to_insert
            if active_length < 0:
                active_length = 0

        prev_split_node_index = -1
        while remainder > 0:
            if active_node.next[active_edge_char] == -1:
                # insert leaf
                # suffix_tree[node_count] = Node(node_count, active_edge_index, len_text, active_node.index)
                suffix_tree[node_count] = Node(node_count, active_edge_index, len_text)
                active_node.next[active_edge_char] = node_count
                # rule 2
                if prev_split_node_index != -1:
                    suffix_tree[prev_split_node_index].link = active_node.index
                prev_split_node_index = node_count
                node_count += 1

                remainder -= 1
                # rule 1
                if active_node.index == 0:
                    active_edge_index += 1
                    if active_edge_index < len_text:
                        active_edge_char = text[active_edge_index]
                    active_length -= 1
                # rule 3
                else:
                    active_node = suffix_tree[active_node.link]
                continue

            split_node = suffix_tree[active_node.next[active_edge_char]]
            if active_length >= split_node.length:
                active_node = split_node
                active_length -= active_node.length
                active_edge_index += active_node.length
                active_edge_char = text[active_edge_index]
                # instead of inserting leaf just rerun the while-loop with the same remainder value
                continue

            if text[split_node.left + active_length] == char_to_insert:
                # Observation: When the final suffix we need to insert is found to exist in the tree already,
                # the tree itself is not changed at all (we only update the active point and remainder)
                # remainder and active edge were updated at the beginning, so need to update only active_length
                active_length += 1
                # rule 2
                if prev_split_node_index != -1:
                    suffix_tree[prev_split_node_index].link = active_node.index
                break

            # create middle node and connect it to active
            # suffix_tree[node_count] = Node(node_count, split_node.left, split_node.left + active_length,
            #                                active_node.index)
            suffix_tree[node_count] = Node(node_count, split_node.left, split_node.left + active_length)
            active_node.next[active_edge_char] = node_count
            mid_node = suffix_tree[node_count]
            node_count += 1
            # create leaf and connect it to middle node
            # suffix_tree[node_count] = Node(node_count, i, len_text, mid_node.index)
            suffix_tree[node_count] = Node(node_count, i, len_text)
            mid_node.next[char_to_insert] = node_count
            node_count += 1
            # update split node and connect it to middle
            split_node.left += active_length
            mid_node.next[text[split_node.left]] = split_node.index
            # split_node.parent = mid_node.index

            remainder -= 1
            # rule 2
            if prev_split_node_index != -1:
                suffix_tree[prev_split_node_index].link = mid_node.index
            prev_split_node_index = mid_node.index
            # rule 1
            if active_node.index == 0:
                active_edge_index += 1
                if active_edge_index < len_text:
                    active_edge_char = text[active_edge_index]
                active_length -= 1
            # rule 3
            else:
                active_node = suffix_tree[active_node.link]

    # for i in range(node_count):
    #     node = suffix_tree[i]
    #     print("\n" + str(node.index) + " " + node.suffix + " " + str(node.next) + " " + str(node.parent))

    edges = []
    for i in range(1, node_count):
        current_node = suffix_tree[i]
        edges.append(text[current_node.left:current_node.right])
    return edges


if __name__ == '__main__':
    # A string Text ending with a “$” symbol
    text = sys.stdin.readline().strip()
    result = build_suffix_tree(text)
    print("\n".join(result))

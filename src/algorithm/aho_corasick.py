import collections

class TrieNode:
    """
    Represents a single node in the Aho-Corasick trie.
    Each node is a state in the finite automaton.
    """
    def __init__(self, node_id):
        self.id = node_id
        
        self.children = {}
        
        self.output = []
        
        self.failure = 0
        
        self.parent = None


class AhoCorasick:
    """
    An implementation of the Aho-Corasick algorithm for efficient multi-pattern string matching.
    It builds a finite automaton from a set of keywords and then processes a text in a single pass.
    """
    def __init__(self):
        self.nodes = [TrieNode(0)]
        self._node_count = 1
        self._finalized = False

    def _get_new_node(self, parent_id=None):
        """Helper to create a new node and add it to our list of nodes."""
        new_node = TrieNode(self._node_count)
        new_node.parent = parent_id
        self.nodes.append(new_node)
        self._node_count += 1
        return new_node.id

    def add_pattern(self, pattern: str):
        """
        Inserts a pattern into the trie.
        This builds the basic keyword tree structure.
        """
        if not pattern:
            return
            
        if self._finalized:
            raise ValueError("Cannot add new patterns after building failure links.")

        current_node_id = 0
        for char in pattern:
            current_node = self.nodes[current_node_id]
            if char not in current_node.children:
                new_node_id = self._get_new_node(parent_id=current_node_id)
                current_node.children[char] = new_node_id
            current_node_id = current_node.children[char]
        
        # The pattern ends at this node, so add it to the output list.
        self.nodes[current_node_id].output.append(pattern)

    def build_failure_links(self):
        """
        Constructs the failure links for the entire trie.
        This must be called after all patterns have been added and before searching.
        This process uses a Breadth-First Search (BFS) approach.
        """
        queue = collections.deque()

        root = self.nodes[0]
        for child_id in root.children.values():
            self.nodes[child_id].failure = 0
            queue.append(child_id)

        while queue:
            current_node_id = queue.popleft()
            current_node = self.nodes[current_node_id]

            for char, next_node_id in current_node.children.items():
                failure_id = current_node.failure

                while char not in self.nodes[failure_id].children and failure_id != 0:
                    failure_id = self.nodes[failure_id].failure

                if char in self.nodes[failure_id].children:
                    self.nodes[next_node_id].failure = self.nodes[failure_id].children[char]
                else:
                    self.nodes[next_node_id].failure = 0

                failure_output_node_id = self.nodes[next_node_id].failure
                self.nodes[next_node_id].output.extend(self.nodes[failure_output_node_id].output)
                
                queue.append(next_node_id)

        self._finalized = True


    def search(self, text: str) -> list[tuple[int, str]]:
        """
        Searches for all added patterns within the given text.

        Args:
            text: The string to search within.

        Returns:
            A list of tuples, where each tuple contains (start_index, matched_pattern).
            The list is not guaranteed to be in any specific order.
        """
        if not self._finalized:
            raise ValueError("Failure links must be built before searching. Call build_failure_links().")

        results = []
        current_node_id = 0

        for i, char in enumerate(text):
            while char not in self.nodes[current_node_id].children and current_node_id != 0:
                current_node_id = self.nodes[current_node_id].failure
            
            if char in self.nodes[current_node_id].children:
                current_node_id = self.nodes[current_node_id].children[char]
            else:
                current_node_id = 0
            
            if self.nodes[current_node_id].output:
                for pattern in self.nodes[current_node_id].output:
                    start_index = i - len(pattern) + 1
                    results.append((start_index, pattern))
        
        return results
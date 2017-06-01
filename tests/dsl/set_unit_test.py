import unittest

from pysie.dsl.set import TernarySearchTrie


class TernarySearchTrieUnitTest(unittest.TestCase):

    def test_map(self):
        trie = TernarySearchTrie()
        self.assertTrue(trie.is_empty())
        trie.put('hello', 'world')
        self.assertTrue(trie.contains_key('hello'))
        self.assertEqual(trie.get('hello'), 'world')
        trie.put('hi', 'there')
        self.assertTrue(trie.contains_key('hi'))
        self.assertEqual(trie.get('hi'), 'there')
        self.assertEqual(trie.size(), 2)
        for i in range(100):
            trie.put(str(i), i)
            self.assertTrue(trie.contains_key(str(i)))
        self.assertEqual(trie.size(), 102)
        trie.delete('hi')
        self.assertFalse(trie.contains_key('hi'))
        self.assertEqual(trie.size(), 101)

        keys = trie.keys()
        self.assertEqual(len(keys), 101)

if __name__ == '__main__':
    unittest.main()
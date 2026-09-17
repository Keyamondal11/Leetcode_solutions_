class Solution(object):
    def minimumHammingDistance(self, source, target, allowedSwaps):
        """
        :type source: List[int]
        :type target: List[int]
        :type allowedSwaps: List[List[int]]
        :rtype: int
        """

        n = len(source)
        parent = list(range(n))

        # Find parent
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        # Union two indices
        def union(a, b):
            rootA = find(a)
            rootB = find(b)

            if rootA != rootB:
                parent[rootA] = rootB

        # Create groups using allowed swaps
        for a, b in allowedSwaps:
            union(a, b)

        # Store source values for each group
        groups = {}

        for i in range(n):
            root = find(i)

            if root not in groups:
                groups[root] = {}

            value = source[i]
            groups[root][value] = groups[root].get(value, 0) + 1

        # Calculate minimum Hamming distance
        answer = 0

        for i in range(n):
            root = find(i)
            value = target[i]

            if groups[root].get(value, 0) > 0:
                groups[root][value] -= 1
            else:
                answer += 1

        return answer
class Solution(object):
    def resultArray(self, nums, k, queries):
        """
        :type nums: List[int]
        :type k: int
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        n = len(nums)

        # Segment tree size
        size = 1
        while size < n:
            size *= 2

        # prod[node] = product of entire segment modulo k
        prod = [1] * (2 * size)

        # cnt[node][r] = number of non-empty prefixes
        # whose product % k == r
        cnt = [[0] * k for _ in range(2 * size)]

        # --------------------------------------------------
        # Merge left segment + right segment
        # --------------------------------------------------
        def pull(node):
            L = node * 2
            R = node * 2 + 1

            # Whole segment product
            prod[node] = (prod[L] * prod[R]) % k

            new_cnt = cnt[L][:]

            # A prefix may contain:
            # entire left segment + prefix of right segment
            left_product = prod[L]

            for r in range(k):
                if cnt[R][r]:
                    nr = (left_product * r) % k
                    new_cnt[nr] += cnt[R][r]

            cnt[node] = new_cnt

        # --------------------------------------------------
        # Build leaves
        # --------------------------------------------------
        for i in range(n):
            pos = size + i
            value = nums[i] % k

            prod[pos] = value
            cnt[pos][value] = 1

        # Build tree
        for node in range(size - 1, 0, -1):
            pull(node)

        # --------------------------------------------------
        # Point update
        # --------------------------------------------------
        def update(index, value):
            pos = size + index

            prod[pos] = value % k
            cnt[pos] = [0] * k
            cnt[pos][value % k] = 1

            pos //= 2

            while pos:
                pull(pos)
                pos //= 2

        # --------------------------------------------------
        # Merge two temporary segment results
        # A followed by B
        # --------------------------------------------------
        def merge(Aprod, Acnt, Bprod, Bcnt):

            result_cnt = Acnt[:]

            for r in range(k):
                if Bcnt[r]:
                    nr = (Aprod * r) % k
                    result_cnt[nr] += Bcnt[r]

            result_prod = (Aprod * Bprod) % k

            return result_prod, result_cnt

        # --------------------------------------------------
        # Query range [l, n-1]
        # --------------------------------------------------
        def range_query(l):
            left = l + size
            right = n - 1 + size

            # Identity / empty segment
            left_prod = 1
            left_cnt = [0] * k

            right_prod = 1
            right_cnt = [0] * k

            while left <= right:

                if left % 2 == 1:
                    left_prod, left_cnt = merge(
                        left_prod,
                        left_cnt,
                        prod[left],
                        cnt[left]
                    )
                    left += 1

                if right % 2 == 0:
                    # This segment comes BEFORE right result
                    right_prod, right_cnt = merge(
                        prod[right],
                        cnt[right],
                        right_prod,
                        right_cnt
                    )
                    right -= 1

                left //= 2
                right //= 2

            final_prod, final_cnt = merge(
                left_prod,
                left_cnt,
                right_prod,
                right_cnt
            )

            return final_cnt

        # --------------------------------------------------
        # Process queries
        # --------------------------------------------------
        result = []

        for index, value, start, x in queries:

            # Persistent update
            nums[index] = value
            update(index, value)

            # After removing prefix [0 ... start-1],
            # remaining array is nums[start ... n-1]
            counts = range_query(start)

            result.append(counts[x])

        return result
        
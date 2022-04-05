import re


class Find:

    @staticmethod
    def leftSpaceCount(str):
        brCount = 0
        count = 0
        spaceStr = re.match('^([\n\s\r]+)\w?', str)
        if spaceStr is not None:
            brCount = spaceStr.group().count('\t')
            count = spaceStr.group().count(' ')
        count = (brCount * 4) + count
        return count

    @staticmethod
    def findAll(sub, s):
        indexList = []
        index = s.find(sub)
        while index != -1:
            indexList.append(index)
            index = s.find(sub, index + 1)
        if len(indexList) > 0:
            return indexList
        else:
            return -1

    @staticmethod
    def minEditDistance(s1, s2):
        if len(s1) == 0:
            return len(s2)
        if len(s2) == 0:
            return len(s1)
        dp = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
        for i in range(len(s1) + 1):
            dp[i][0] = i
        for j in range(len(s2) + 1):
            dp[0][j] = j
        for i in range(1, len(s1) + 1):
            for j in range(1, len(s2) + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]) + 1
        return dp[len(s1)][len(s2)]

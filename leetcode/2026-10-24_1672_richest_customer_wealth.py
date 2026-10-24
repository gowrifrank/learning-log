# LeetCode 1672. Richest Customer Wealth (Easy)
# https://leetcode.com/problems/richest-customer-wealth/
# 2026-10-24: nested list + ACCUMULATOR per customer + BEST SO FAR

class Solution:
    def maximumWealth(self, accounts: list[list[int]]) -> int:
        temp_acc = []
        balance = 0
        winner = 0
        for account in accounts:
            temp_acc = account

            for i in range(len(temp_acc)):
                balance += temp_acc[i]

            if balance > winner:
                winner = balance

            balance = 0

        return winner

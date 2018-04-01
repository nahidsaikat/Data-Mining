from k_means import DBScanner

scanner = DBScanner(0.1, 5)
scanner.db_scan()

test_case_1 = set([1, 2, 3, 4, 5, 6, 7, 8, 9, -1])
clusters = scanner.get_clusters()

print 'Test Case # 1'
print test_case_1
print clusters


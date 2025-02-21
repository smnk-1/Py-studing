from BloomCountFilter import BloomCountFilter

bcf = BloomCountFilter(10, 2)
print(bcf.count_array)
bcf.add('banana')
print(bcf.count_array)
bcf.add('banana')
print(bcf.count_array)

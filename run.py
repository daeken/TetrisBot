from ga import GA

ga = GA(10, 16, 2, 1, 3, 5, 0.1)

print ga.batch
ga.next()
print ga.batch

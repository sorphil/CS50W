test_list = ['CSS', 'Django', 'Git', 'HTML', 'Python']
  
# printing original list  
print ("The original list is : " + str(test_list)) 
  
# initializing substring 
subs = ''
  
# using list comprehension  
# to get string with substring  
res = [i for i in test_list if subs in i] 
  
# printing result  
print ("All strings with given substring are : " + str(res)) 
1. List Operations
  fruits = ["apple","banana","mango","orange"]
  fruits.append("pineapple")
  fruits.remove("banana")
  fruits[1]="kiwi"

  print("Final list:",fruits)
  print("Length:",len(fruits))


2. Tuple Analysis
    tup = (1,2,3,4,2,2)
    print(tup)
      print(tup.count(2))
      print(tup.index(3))

3. SET Behavior
    s={1,2,3,2,4,1}
    print(s)
      s.add(5)
      s.remove(3)
      s.discard(10)
    print("Updated set : ",s)


4. Dictionary Manipulation
    student = {
       "name": "John",
        "email":"John@gmail.com",
        "phone":"12345678"
        }
      print(student.keys())
      print(student.values())
    student["name"]="Mike"
    student["address"]="New York"
    print(student.get("name"))


5.Nested Dictionary
    student = {
       "name": "John",
        "subjects":{
                "math":90,
                "science":85
        }
      }
        print(student["subjects"]["math"]
        student["subjects"]["english"] = 88
        print(student)

6. Unpacking and *Operator
    vegetables = ["carrot","potato","tomato","onion","peas"]
        v1,v2,*rest = vegetables
      print(v1)
      print(v2)
      print(rest)


7. Membership and Identity Operators
    1st = [1,2,3,4,5]
        print(2 in 1st)
    a = [1,2,3]
    b= [1,2,3]
    print(a==b)
    print(a is b)

8. Shallow and Deep COpy
    import copy
    nested = [[1,2],[3,4]]
    shallow = copy.copy(nested)
    deep = copy.deepcopy(nested)
    nested[0][0] =100
    print("original:",nested)
    print("shallow:", shallow)
    print(deep)


9. Logical and bitwise
    a =true
    b=false
    print(a and b)
    print(a or b)
    print(not a)

    x =5
    y=3
    print(x&y)
    print(x|y)
    print(x^y)
    print(~x)

10. Looping Through Data Structures

    1st = [1,2,3]
    for item in 1st:
        print(item)
        d = {"a":1,"b":2}
        for key in d:
              print("Key:",key)
        for(value in d.values():
              print("Values:",value)
        for k,v in d.items():
                print(k,v)


  

# RSL Language (Ryve Simple Language)
### simple language that build with python  
---
## Versions  

> ### **v0.1**
- Tokenizer

> ### **v0.31**
- Tokenizer with type

> ### **v0.48**
- Tokenizer with keywords
- New Keywword & feauture
  - #### **var**  
    grammar:  
      `var <variable-name> = <variable-value>` 

    usage:  
      ```
      var x = 5  
      var str = "String"
      ```
  - #### **stdout**
    grammar:  
      `stdout <variable-name>`
      `stdout <args>` 

    usage:  
      ```
      var y = 100
      stdout y
      // output 100
      ```

> ### **v0.72**
- New Keyword
  - #### **fun: void! (no return)**  
    grammar:  
      `fun <function-name>(<args>)`
      &nbsp;&nbsp;&nbsp;&nbsp;`<code>`  
      `end` 

    usage:  
      ```
      fun say_hello()
        print("hello")
      end

      fun hello(name)
        print("Hello, " + name)
      end
      ```
  - #### **type**:
    grammar:  
      `type(<variable-name>)` 

    usage:  
      ```
      var x = 5
      type(x) // INT
      var ryve = "Hello World"
      type(ryve) // STRING
      ```

- Variable changing value  
  before:
    ```
    var x = 10
    print(x) // 10
    var x = 5
    print(x) // 10
    ```
  now:  
    ```
    var x = 10
    print(x) // 10
    var x = 5
    print(x) // 5
    #you can also do this
    var x = 5
    var x = x * x
    print(x) // 25
    ```

- Variable deliver   
  before:
    ```
    var x = 10
    print(x) // x
    ```
  after:  
    ```
    var x = 10
    print(x) // 10
    ```

> ### **v0.82**
- New Keyword
  - #### **allvar**  
    printing all variables in memory  
    usage:  
      ```
      allvar
      allvar() <- Better way
      ```

  - #### **free**
    delete variable in memory  
    grammar:  
    `free(<variable-name>)`  

    usage:  
      ```
      var x = 5
      free(x)
      // now 'x' variable was deleted
      ```

  - #### **print**
    print something to screen  
    grammar:  
    `print(<argument>)`  

    usage:
      ```
      var ryve = "hello"
      print(ryve)
      ```

  - #### **repeat**  
    repeating function  
    grammar:  
    `repeat(<times>, <function-name>)`  

    usage:  
      ```
      fun hello()
        print("hello world")
      end
      repeat(4, hello())
      repeat(6, hello())
      ```
      
- Better Parser & Parser fix (now parser can receive STRING type)
- Now function can return something  
  ```
  fun add(x, y)
    return x + y
  end
  var x = add(10, 8)
  print(x) // 18
  ```

- Comments!
  ```
  # Hello
  # Ryve
  ```
---
## Running
> ### **Requirements**
  - Python 3.7+
  - Colorama Module (for better looks)
> ### **How to run**
  - Shell Mode  
    ```
    $ rsl
    ```  
  - Run from file
    ```
    $ rsl <filename>.rsl
    ```
  - Check version
    - Method 1 (via shell)  
      ```
      $ rsl
      "RSL v0.82, release: 22 June 2022"
      "Rsl ver 0.82 22-06-22"
      ```
    - Method 2 (via argument)  
      ```
      $ rsl -v
      Rsl 0.82
      ```
-- Factorial
factorial :: Integer -> Integer
factorial 0 = 1
factorial n = n * factorial(n - 1)

-- Fibonacci
fibonacci :: Integer -> Integer
fibonacci 0 = 0
fibonacci 1 = 1
fibonacci n = fibonacci(n - 1) + fibonacci(n - 2)

-- Absolute Value
absValue :: Int -> Int
absValue x
    | x >= 0 = x
    | otherwise = -x

-- Power b ^ e
-- b = base
-- e = exponent
power :: Int -> Int -> Int
power b 0 = 1
power b e
    | even e = n * n
    | otherwise = n * n * b
    where
        n = power b (e `div` 2)


-- Is Prime Number
isPrime :: Int -> Bool
isPrime 0 = False
isPrime 1 = False
isPrime x  = not (hasDivisor (x-1))
    where
        hasDivisor :: Int -> Bool
        hasDivisor 1 = False
        hasDivisor n = mod x n == 0 || hasDivisor(n-1)


-- Pop the last element from the list
popBack :: [a] -> a
popBack [] = error "Empty List"
popBack [x] = x
popBack (_:xs) = pop xs

-- Pop the front element from the list
popFront :: [a] -> a
popFront [] = error "Emtpy List"
popFront [x] = x
popFront [head:tail] = head


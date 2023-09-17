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




//! This module contains solutions to exercises of the arrays and strings section of the book

/// Implement an algorithm to determine if a string has all unique characters.
/// What if you cannot use additional data structures?
/// exercise 1.1.
pub mod exercise_1 {

    use std::collections::HashSet;

    pub fn has_unique_characters<T: AsRef<str>>(string: T) -> bool {
        let mut set: HashSet<char> = std::collections::HashSet::new();
        string
            .as_ref()
            .chars()
            .map(|c| set.insert(c))
            .fold(true, |acc, x| acc & x)
    }

    pub fn has_unique_characters_raw(string: &str) -> bool {
        let mut ascii: [usize; 128] = [0; 128];
        for c in string.chars() {
            let index: usize = c as usize;
            ascii[index] = ascii[index] + 1;
        }
        for v in &ascii {
            if v > &1 {
                return false;
            }
        }
        true
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[test]
        fn test_unique_characters_with_unique_characters() {
            let input = "abcde";
            assert_eq!(true, has_unique_characters(input));
            assert_eq!(true, has_unique_characters(String::from(input)));
            assert_eq!(true, has_unique_characters(&String::from(input)));
        }

        #[test]
        fn test_unique_characters_with_non_unique_characters() {
            let input = "abcdea";
            assert_eq!(false, has_unique_characters(input));
            assert_eq!(false, has_unique_characters(String::from(input)));
            assert_eq!(false, has_unique_characters(&String::from(input)));
        }

        #[test]
        fn test_unique_characters_raw_with_unique_characters() {
            let input = "abcde";
            assert_eq!(true, has_unique_characters_raw(input));
            assert_eq!(true, has_unique_characters_raw(&String::from(input)));
        }

        #[test]
        fn test_unique_characters_raw_with_non_unique_characters() {
            let input = "abcdea";
            assert_eq!(false, has_unique_characters_raw(input));
            assert_eq!(false, has_unique_characters_raw(&String::from(input)));
        }
    }
}

/// Implement a function void reverse(char* str) in C or C++ which reverses a null- terminated string.
/// exercise 1.2
pub mod exercise_2 {

    pub fn reverse_string(string: &str) -> String {
        string.chars().rev().collect()
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[test]
        fn test_reverse_string() {
            let input = "abcd";
            let expected = "dcba";
            assert_eq!(expected, reverse_string(input));
            assert_eq!(expected, reverse_string(&String::from(input)));
        }
    }
}

/// Given two strings, write a method to decide if one is a permutation of the other.
/// exercise 1.3
pub mod exercise_3 {
    fn is_permutation(s1: &str, s2: &str) -> bool {
        if s1.len() != s2.len() {
            return false;
        }
        let mut map: std::collections::HashMap<char, i32> = std::collections::HashMap::new();
        s1.chars().clone().for_each(|c| match map.get_mut(&c) {
            Some(v) => {
                *v += 1;
            }
            None => {
                map.insert(c, 1);
            }
        });
        s2.chars().clone().for_each(|c| match map.get_mut(&c) {
            Some(v) => {
                *v -= 1;
            }
            _ => (),
        });
        map.iter()
            .fold(0, |acc: i32, (_key, value)| -> i32 { acc + value })
            == 0i32
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[test]
        fn test_is_permutation_on_permutations() {
            let s1 = "abdca";
            let s2 = "dcbaa";
            assert!(is_permutation(s1, s2))
        }

        #[test]
        fn test_is_permutation_on_none_permutations() {
            // different length
            {
                let s1 = "abdc";
                let s2 = "dcb";
                assert!(!is_permutation(s1, s2))
            }
            // different elements
            {
                let s1 = "abdc";
                let s2 = "dcbz";
                assert!(!is_permutation(s1, s2))
            }
        }
    }
}

/// Write a method to replace all spaces in a string with'%20'.
/// You may assume that the string has sufficient space at the end of the string
/// to hold the additional characters, and that you are given
/// the "true" length of the string. (Note: if imple- menting in Java,
/// please use a character array so that you can perform this opera- tion in place.)
///
/// EXAMPLE
/// Input: "Mr John Smith Output: "Mr%20Dohn%20Smith"
///
/// exercise 1.4
pub mod exercise_4 {
    fn replace_spaces(string: &str) -> String {
        string.replace(" ", "%20")
    }

    #[cfg(test)]
    mod tests {
        use super::*;
        #[test]
        fn test_replace_spaces() {
            let input = "Mr John Smith";
            let expected = "Mr%20John%20Smith";
            assert_eq!(expected, replace_spaces(input));
        }
    }
}

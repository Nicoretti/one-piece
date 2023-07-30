//! This module contains solutions to exercises of the chapter/section linked lists

/// Linked list implementation 2.0
pub mod exercise_2_0 {

    #[derive(Debug)]
    pub struct List<T> {
        head: Link<T>,
    }

    type Link<T> = Option<Box<Node<T>>>;

    #[derive(Debug)]
    struct Node<T> {
        element: T,
        next: Link<T>,
    }

    impl<T: Default> Node<T> {
        pub fn new(value: T) -> Self {
            Self {
                element: value,
                next: Link::None,
            }
        }
    }

    impl<T: Default> List<T> {
        pub fn new() -> Self {
            Self { head: Link::None }
        }

        pub fn push_front(&mut self, value: T) {
            let node = Box::new(Node {
                element: value,
                next: self.head.take(),
            });
            self.head = Link::Some(node);
        }

        pub fn pop_front(&mut self) -> Option<T> {
            self.head.take().map(|node| {
                self.head = node.next;
                node.element
            })
        }

        pub fn peek(&self) -> Option<&T> {
            self.head.as_ref().map(|node| &node.element)
        }

        pub fn peek_mut(&mut self) -> Option<&mut T> {
            self.head.as_mut().map(|node| &mut node.element)
        }
    }

    impl<T> Drop for List<T> {
        fn drop(&mut self) {
            let mut current_link = self.head.take();
            while let Some(mut boxed_node) = current_link {
                current_link = boxed_node.next.take()
            }
        }
    }

    #[cfg(test)]
    mod tests {

        use super::*;

        #[test]
        fn test_smoke_test() {
            let mut list: List<u32> = List::new();

            assert_eq!(list.pop_front(), None);

            list.push_front(1u32);
            list.push_front(2u32);
            list.push_front(3u32);

            assert_eq!(list.pop_front(), Some(3u32));
            assert_eq!(list.pop_front(), Some(2u32));
            assert_eq!(list.pop_front(), Some(1u32));
            assert_eq!(list.pop_front(), None);
        }

        #[test]
        fn test_peek() {
            let mut list: List<u32> = List::new();

            assert_eq!(list.peek(), None);

            list.push_front(2);
            assert_eq!(list.peek(), Some(&2u32));

            list.push_front(3);
            assert_eq!(list.peek(), Some(&3u32));
        }

        #[test]
        fn test_peek_mut() {
            let mut list: List<u32> = List::new();

            assert_eq!(list.peek(), None);
            list.push_front(2);
            assert_eq!(list.peek_mut(), Some(&mut 2u32));
            list.peek_mut().map(|v| *v = 4u32);
            assert_eq!(list.peek(), Some(&4u32));
        }
    }
}

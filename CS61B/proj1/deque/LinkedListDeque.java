package deque;

import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

public class LinkedListDeque<T> implements Deque<T>, Iterable<T>{
    private Node sentinel;
    private int size;

    public class Node {
        private T item;
        private Node next;
        private Node prev;

        public Node(T item, Node prev, Node next) {
            this.item = item;
            this.prev = prev;
            this.next = next;
        }


    }

    private class LinkedListIterator implements Iterator<T> {
        Node currentNode = sentinel.next;

        @Override
        public boolean hasNext() {
            return currentNode != sentinel;
        }

        public T next() {
            if (!hasNext()) {
                return null;
            }

            T item = currentNode.item;
            currentNode = currentNode.next;
            return item;
        }

        public Iterator<T> iterator() {
            return LinkedListIterator();
        }

        public void initializeSentinel() {
            size = 0;
            sentinel = new Node(-1000, null, null);
            sentinel.next = sentienl;
            sentinel.prev = sentinel;
        }


        // 여기가 Constructor for LinkedListDeque class
        public LinkedListDeque() {
            initializeSentinel();
        }

        public LinkedListDeque(T item) {
            initializeSentinel();
            this.addFirst(item);
        }


        // Methods overriding from Deque<T> interface
        @Override
        public void addFirst(T item) {
            siez++;
            Node newNode = new Node(item, sentinel, sentinel.next);
            sentinel.next.prev = newNode;
            sentinel.next = newNode;
        }

        @Override
        public void addLast(T item) {
            size++;
            // 12/23 (not solved) : 여기서 sentinel.prev 대신 this.next를 사용할수 있는지 체크바람
            Node newNode = new Node(item, sentinel.prev, sentinel);
            sentinel.prev.next = newNode;
            sentinel.prev = newNode;
        }

        @Override
        public int size() {
            return this.size;
        }

        @Override
        public void printDeque() {
            for (int i = 0; i < this.size; i++) {
                T item = this.sentinel.next.item;
                if (this.sentinel.next == sentinel) {
                    System.out.println(item);
                } else {
                    System.out.println(item + " ");
                    this.sentinel.next = this.sentinel.next.next;
                }
            }
            System.out.println('\n');
        }

        @Override
        public T removeFirst() {
            // 내가 직접 만들어서 돌아갈지모름. (Solved!)
            if (sentinel.next == sentinel) {
                return null;
            } else {
                T item = sentinel.next.item;
                Node afterRemoved = sentinel.next.next;
                // 12/25(not solved) 이걸로 삭제 가능? 내가 생각한거 (Solved!)
                sentinel.next = sentinel.next.next;
                afterRemoved.prev = sentinel;
                this.size--;
                return item;
            }
        }
// Pointer에 대해서 헷갈려서 설명하자면 remove하는 상황에 아무 pointer가 자신을 지정하고 있지않은 node는 garbage collected 당함.
// 이 아래 코드를 java visualizer에 해보면 나옴
// public class ClassNameHere {
//     public static void main(String[] args) {

//         Node nodefan1 = new Node(1, null, null);
//         nodefan1.next = new Node(2, null, nodefan1);
//         nodefan1.next.next = new Node(3, null, nodefan1.next);
//         nodefan1.next = nodefan1.next.next;
//         nodefan1.next.prev = nodefan1;
//     }

//     public static class Node {
//         int item;
//         Node next;
//         Node prev;

//         public Node(int item, Node next, Node prev) {
//             this.item = item;
//             this.next = next;
//             this.prev = prev;
//         }
//     }
// }

        @Override
        public T removeLast() {
            if (sentinel.next == sentinel) {
                return null;
            } else {
                T item = sentinel.prev.item;
                // 12/25(not solved) 이걸로 삭제 가능? 내가 생각한거
                sentinel.prev = sentinel.prev.prev;
                sentinel.prev.next = sentinel;
                this.size--;
                return item;
            }
        }

        @Override
        public T get(int index) {
            if (index >= this.size) {
                return null;
            }
            Node current = sentinel.next;
            for (int i = 0; i < index; i++) {
                current = current.next;
            }
            return current.item;
        }

        @Override
        public boolean equals(Object o) {
            if (o == null) {
                return false;
            } else if (o == this) {
                return true;
            } else if (o instanceof Deque) {
                Deque<T> casted_o = Deque<T> o;
                // First, check the size of two
                // Deque.java also have size() so you can youse Deque<T> o.size()
                if (this.size() != casted_o.size()) {
                    return false;
                }

                for (int i = 0; i < this.size(); i++) {
                    if (!(this.get(i).equals(casted_o.get(i)))) {
                        return false;
                    }
                }
                return true;

            }
        }







    }


}

#include <cstdio>
#include <cstdlib>
#include <unistd.h>
#include <list>
#include <vector>
#include <queue>
#include <stack>
#include <cstring>
#define DATA_SIZE 0x98
#define MAX_NUM 2

int get_num() {
    char buf[8];
    int t = read(0, buf, 7);
    buf[t] = '\0';
    return atoi(buf);
}

class Test {
    public:
        char* data;
        Test() {
            data = NULL;
        }
        Test(const Test& obj) {
            if(obj.data) {
                data = (char*)malloc(DATA_SIZE);
                memcpy(data, obj.data, DATA_SIZE);
            }
        }
        ~Test() {
            free(data);
        }
        void Init() {
            data = (char*)malloc(DATA_SIZE);
            printf("input data:");
            read(0, data, DATA_SIZE);
        }
};

std::list<Test>* mList;
std::vector<Test>* mVector;
std::queue<Test>* mQueue;
std::stack<Test>* mStack;

void init_proc() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    mList = new std::list<Test>;
    mVector = new std::vector<Test>;
    mQueue = new std::queue<Test>;
    mStack = new std::stack<Test>;
    Test t;
    for(int i=0; i<2;i++){
        mList->push_back(t);
        mVector->push_back(t);
        mQueue->push(t);
        mStack->push(t);
    }
    for(int i=0; i<2;i++){
        mList->pop_back();
        mVector->pop_back();
        mQueue->pop();
        mStack->pop();
    }
    alarm(60);
}

void menu() {
    puts("STL Container Test");
    puts("1. list");
    puts("2. vector");
    puts("3. queue");
    puts("4. stack");
    puts("5. exit");
    printf(">> ");
}

void submenu() {
    puts("1. add");
    puts("2. delete");
    puts("3. show");
    printf(">> ");
}

void TestList() {
    submenu();
    int choice = get_num();
    switch(choice) {
        case 1:{
            if(mList->size()>=MAX_NUM) {
                puts("full!");
                return;
            }
            Test t;
            t.Init();
            mList->push_back(t);
            puts("done!");
        }
        break;
        case 2:{
            puts("index?");
            unsigned int index = get_num();
            if(index >= mList->size()) {
                puts("invalid index!");
                return;
            }
            std::list<Test>::iterator t = mList->begin();
            for(int i=0; i < index; i++)
                t++;
            mList->erase(t);
            puts("done!");
        }
        break;
        case 3:{
            puts("index?");
            unsigned int index = get_num();
            if(index >= mList->size()) {
                puts("invalid index!");
                return;
            }
            std::list<Test>::iterator t = mList->begin();
            for(int i=0; i < index; i++)
                t++;
            printf("data: %s\n", t->data);
        }
        break;
        default:
            puts("invalid choice!");
    }
}

void TestVector() {
    submenu();
    int choice = get_num();
    switch(choice) {
        case 1: {
            if(mVector->size()>=MAX_NUM) {
                puts("full!");
                return;
            }
            Test t;
            t.Init();
            mVector->push_back(t);
            puts("done!");
        }
        break;
        case 2:{
            puts("index?");
            unsigned int index = get_num();
            if(index >= mVector->size()) {
                puts("invalid index!");
                return;
            }
            std::vector<Test>::iterator t = mVector->begin();
            for(int i=0; i < index; i++)
                t++;
            mVector->erase(t);
            puts("done!");
        }
        break;
        case 3:{
            puts("index?");
            unsigned int index = get_num();
            if(index >= mVector->size()) {
                puts("invalid index!");
                return;
            }
            std::vector<Test>::iterator t = mVector->begin();
            for(int i=0; i < index; i++)
                t++;
            printf("data: %s\n", t->data);
        }
        break;
        default:
            puts("invalid choice!");
    }
}

void TestQueue() {
    submenu();
    int choice = get_num();
    switch(choice) {
        case 1:{
            if(mQueue->size()>=MAX_NUM) {
                puts("full!");
                return;
            }
            Test t;
            t.Init();
            mQueue->push(t);
            puts("done!");
        }
        break;
        case 2:{
            if(mQueue->size()) {
                mQueue->pop();
            } else {
                puts("empty!");
            }
            puts("done!");
        }
        break;
        case 3:{
            puts("not supported!");
        }
        break;
        default:
            puts("invalid choice!");
    }
}

void TestStack() {
    submenu();
    int choice = get_num();
    switch(choice) {
        case 1:{
            if(mStack->size()>=MAX_NUM) {
                puts("full!");
                return;
            }
            Test t;
            t.Init();
            mStack->push(t);
            puts("done!");
        }
        break;
        case 2:{
            if(mStack->size()){
                mStack->pop();
            } else {
                puts("empty!");
            }
            puts("done!");
        }
        break;
        case 3:{
            puts("not supported!");
        }
        break;
        default:
            puts("invalid choice!");
    }
}

int main() {
    init_proc();
    while(1) {
        menu();
        int choice = get_num();
        switch(choice) {
            case 1:
                TestList();
                break;
            case 2:
                TestVector();
                break;
            case 3:
                TestQueue();
                break;
            case 4:
                TestStack();
                break;
            case 5:
                exit(0);
            default:
                puts("invalid choice");
        }
    }
    return 0;
}

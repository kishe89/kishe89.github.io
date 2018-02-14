---
layout: post
title:  "JavaScript callback-3"
date:   2018-02-14 15:32:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Javascript
---

```
자바스크립트 패턴과 테스트
길벗출판사,(지은이) 래리 스펜서, 세스 리처즈 ,(옮긴이) 이일웅
```
참고

[Javascript callback-1],[Javascript callback-2] 에서는 콜백에 대한 내용과 비동기 함수 및 콜백의 실행순서를 보장하기 위한 기법들을 알아보았다.

앞에서 작성하던 계산기 예제를 이어가본다.

### Calculator 작성
---

[Javascript callback-1] 에서 작성중이던 Calculator05 를 보도록 한다.

##### Calculator05
```javascript
Calculator.prototype.add = (...args)=>{
    let result = 0;
    args.forEach((value)=>{
        if(Array.isArray(value)){
            result += Calculator.prototype.add(...value);
            return;
        }
        result+=value;
    });
    return result;
};
```

전달된 매개변수들에 대해서 덧셈은 정상적으로 작동한다.

단 전달된 매개변수들이 Number 여야만 정상적으로 동작한다.

문자열등이 들어온다거나 했을 때 예기치 못한 응답값을 뱉을 것이다.

일단 테스트를 작성해본다.

##### Calculator_tests
```javascript
describe('Calculator',()=>{
    let myApp;
    const dummyArray = [
        1,2,3,4,5,6,7,8,9,10
    ];
    const dummyNdepthArray = [
        1,2,3,4,5,6,7,8,9,10,
        [
            1,2,3,4,5,6,7,8,9,10,
            [
                1,2,3,4,5,6,7,8,9,10
            ]
        ]
    ];
    const badArguments = [
        1,'a',undefined,3,[],true,function () {console.log('a');}
    ];
    beforeEach(()=>{
        myApp = new MyApp();
        myApp.setCalculator(new Calculator());
    });

    describe('Calculator.add()',()=>{

        it('integer parameters add',()=>{
            const result= myApp.calculator.add(1,2,3);
            expect(result).toBe(6);
        });
        it('integer parameters | ArrayParameter add',()=>{
            const result= myApp.calculator.add(1,2,dummyArray);
            expect(result).toBe(58);
        });
        it('N depth ArrayParameter add',()=>{
            const result= myApp.calculator.add(1,2,dummyNdepthArray);
            expect(result).toBe(168);
        });
        it('Other type add',()=>{
            const result= myApp.calculator.add(badArguments);
            expect(result).toBe('');
        });
    });
});
```
Other type add 테스트는 실패하게 된다.

badArguments 에는 정상적인 argument 인 1,3 을 제외하고 String, undefined,empty array, Function 이 들어가있다.

테스트 결과는 아래처럼 나올것이다.

##### Caculator.html 실행결과
![Alt text](/assets/javascript_tdd_image/ex5/index6.png)

반환 결과로 **'01aundefined30truefunction () {console.log('a');}'** 문자열이 반환되었다.

Number 를 제외한 값들은 더하지 않도록 Calculator05에 코드를 추가한다.

그리고 테스트도 수정하도록 한다. 정상적인 argument 1,3 의 합인 4로 변경하도록한다.

##### Calculator06
```javascript
Calculator.prototype.add = (...args)=>{
    let result = 0;
    args.forEach((value)=>{
        if(typeof value === 'number'){
            result += value;
        } else if(Array.isArray(value)){
            result += Calculator.prototype.add(...value);
        }
    });
    return result;
};
```
##### Calculator_tests
```javascript
it('Other type add',()=>{
    const result= myApp.calculator.add(badArguments);
    expect(result).toBe(4);
});
```

테스트를 실행해본다.

##### Caculator.html 실행결과
![Alt text](/assets/javascript_tdd_image/ex5/index7.png)

테스트는 성공하게 된다.

하지만 덧셈을 숫자가 아닌 arguments 에 대해 수행할 필요는 없다.

차라리 전달받은 타입이 문제가 있다고 다시 입력해달라고 알려주는 것이 좋을 것이다.

Calculator06 과 Calculator_tests 의 Other type add 테스트를 수정한다.

##### Calculator07
```javascript

Calculator.prototype.add = (...args)=>{
    let result = 0;
    args.forEach((value)=>{
        if(typeof value === 'number'){
            result+=value;
        } else if(Array.isArray(value)){
            result += Calculator.prototype.add(...value);
        } else{
            throw new Error('The argument is invalid.');
        }
    });
    return result;
};
```

##### Calculator_tests
```javascript
it('Other type add',()=>{
    expect(()=>{
        myApp.calculator.add(badArguments);
    }).toThrow();
});
```

toThrow 함수를 이용하여 throw 를 하는지 확인한다.

테스트는 성공한다.

이제 타입에 대해서도 체크를 완료 하였다.

아직 우리는 add 에 **Promise**, **async await** 을 이용하지 않았다.

이제 시작해본다.

### Promise 적용
---

[Javascript callback-1]에서 저장 부분과 계산 부분을 나눈다고 이야기했다.

Calculator07 을 아래처럼 수정하도록 한다.

##### Calculator08
```javascript
Calculator.prototype.add = (...args)=>{
    let result = 0;
    args.forEach((value)=>{
        if(typeof value === 'number'){
            result+=value;
        } else if(Array.isArray(value)){
            result += Calculator.prototype.add(...value);
        } else{
            throw new Error('The argument is invalid.');
        }
    });
    return Promise.resolve(result);
};
```
saveFunc, renderFunc, etc 들은 비동기 함수의 호출의 연속일 가능성이 높다.

이러한 함수들의 체인 및 실행순서 보장을 쉽게 하기 위해 여태 작성한 add 함수를 thenable 하게 만들어준다.

그리고 테스트를 돌려보도록 한다.

##### Caculator.html 실행결과
![Alt text](/assets/javascript_tdd_image/ex5/index8.png)

이전까지 통과했던 모든 테스트들이 깨졌다.

단 하나 에러를 throw 하길 바라는 테스트만이 성공한다(Aspect 관련 포스팅에서 이야기 했듯이 우연히 성공한 테스트는 무시한다.).

테스트가 깨진 이유는 기존에 우리가 return 하던 값이 아닌 Promise.resolve 로 Promise 를 반환했기 때문이다.

테스트를 수정해보도록 한다.

##### Calculator_tests
```javascript
describe('Calculator',()=>{
    let myApp;
    const dummyArray = [
        1,2,3,4,5,6,7,8,9,10
    ];
    const dummyNdepthArray = [
        1,2,3,4,5,6,7,8,9,10,
        [
            1,2,3,4,5,6,7,8,9,10,
            [
                1,2,3,4,5,6,7,8,9,10
            ]
        ]
    ];
    const badArguments = [
        1,'a',undefined,3,[],true,function () {console.log('a');}
    ];
    beforeEach(()=>{
        myApp = new MyApp();
        myApp.setCalculator(new Calculator());
    });

    describe('Calculator.add()',()=>{

        it('integer parameters add',()=>{
            const result= myApp.calculator.add(1,2,3);
            result.then((value)=>{
                expect(value).toBe(6);
            });
        });
        it('integer parameters | ArrayParameter add',()=>{
            const result= myApp.calculator.add(1,2,dummyArray);
            result.then((value)=>{
                expect(value).toBe(58);
            });
        });
        it('N depth ArrayParameter add',()=>{
            const result= myApp.calculator.add(1,2,dummyNdepthArray);
            result.then((value)=>{
                expect(value).toBe(168);
            });
        });
        it('Other type add',()=>{
            const result = myApp.calculator.add(badArguments);
            result.then((value)=>{

            }).catch((e)=>{
                console.log(e);
                expect(e).toThrowError(new Error('The argument is invalid.'));
            });

        });
    });
});
```

성공했던 테스트도 Promise 의 처리절차에 따라 처리하도록 변경하였다.

이전에 실패하던 테스트는 모두 성공한다.

하지만 이전에 성공하던 에러를 throw 하길 바랬던 테스트는 실패한다.

add 함수에서 우리가 thenable 한 Promise 를 던지는건 정상적으로 처리된 result 에 대해서만 Promise.resolve 로 반환했다.

실패시 즉 throw 시에는 thenable 하지 못하다.

throw 하는 쪽을 아래처럼 수정한다.

##### Calculator09
```javascript
'use strict';
let Calculator = function () {
    if(!(this instanceof Calculator)) {
        return new Error('Call by new');
    }
};

Calculator.prototype.add = (...args)=>{
    let result = 0;
    args.forEach((value)=>{
        if(typeof value === 'number'){
            result+=value;
        } else if(Array.isArray(value)){
            result += Calculator.prototype.add(...value);
        } else{
            Promise.reject(new Error('The argument is invalid.'));
        }
    });
    return Promise.resolve(result);
};
```

그리고 테스트를 실행한다.

##### Calculator.html(Promise 추가 후 테스트화면)
![Alt text](/assets/javascript_tdd_image/ex5/index9.png)

전부 성공한다.

너무 쉽게 해결 된다!!!!!

그런데 이게 과연 진짜로 정말로 맞는 코드일까?

정말 궁금한 마음에 테스트의 then 에 console.log 로 value, e 를 찍어본다.

결과는!!!

##### Calculator.html(console.log 추가 후 개발자도구 콘솔화면)
![Alt text](/assets/javascript_tdd_image/ex5/index10.png)

놀랍다. 테스트 케이스는 모두 통과했는데 실제 값은 number+응답된 Promise 객체가 나와있다.

이것만 믿고 회사에서 '일 끝냈습니다!' 하고 퇴근하면 퇴근하던 지하철에서 다시 출근 지하철로 갈아타야할 수 있다.

이유는 이 함수가 비동기 함수이기 때문이다.

테스트 케이스에 제공된 콜백 함수가 Promise 가 결정되기 전에 종료되면서 발생한 것이다.

```javascript
console.log('before');
console.log('after');
```
각 테스트 케이스의 시작지점과 끝지점에 위 로그를 추가해서 확인해보도록 한다.

##### Calculator_tests
```javascript
describe('Calculator',()=>{
    let myApp;
    const dummyArray = [
        1,2,3,4,5,6,7,8,9,10
    ];
    const dummyNdepthArray = [
        1,2,3,4,5,6,7,8,9,10,
        [
            1,2,3,4,5,6,7,8,9,10,
            [
                1,2,3,4,5,6,7,8,9,10
            ]
        ]
    ];
    const badArguments = [
        1,'a',undefined,3,[],true,function () {console.log('a');}
    ];
    beforeEach(()=>{
        myApp = new MyApp();
        myApp.setCalculator(new Calculator());
    });

    describe('Calculator.add()',()=>{

        it('integer parameters add',()=>{
            console.log('before');
            const result= myApp.calculator.addition(1,2,3);
            result.then((value)=>{
                console.log(value+':'+(value === 6));
                expect(value).toBe(6);
            });
            console.log('after');
        });
        it('integer parameters | ArrayParameter add',()=>{
            console.log('before');
            const result= myApp.calculator.addition(1,2,dummyArray);
            result.then((value)=>{
                console.log(value+':'+(value === 58));
                expect(value).toBe(58);
            });
            console.log('after');
        });
        it('N depth ArrayParameter add',()=>{
            console.log('before');
            const result= myApp.calculator.addition(1,2,dummyNdepthArray);
            result.then((value)=>{
                console.log(value+':'+(value === 168));
                expect(value).toBe(168);
            });
            console.log('after');
        });
        it('Other type add',()=>{
            console.log('before');
            const result = myApp.calculator.addition(badArguments);
            result.then((value)=>{

            }).catch((e)=>{
                console.log(e);
                expect(e).toThrowError(new Error('The argument is invalid.'));
            });
            console.log('after');
        });
    });
});
```

##### Calculator.html(console.log('before&after') 추가 후 개발자도구 콘솔화면)
![Alt text](/assets/javascript_tdd_image/ex5/index11.png)

콘솔창을 보면 expect 는 테스트케이스가 완료된 후 호출되고 있다.

Jasmine 에서는 비동기함수의 테스트를 서포팅하기 위해서 done 을 호출하라고 문서에서 안내하고있다.
이 done 의 호출에 따라 beforeEach, afterEach 등의 함수들의 실행도 되게 된다.

기본적으로 5초의 타임아웃 시간이 있으나 이를 beforeEach 와 afterEach 에서 타임을 변경하여 사용가능하다.

어쨋든 done 을 호출해줘야 정상적으로 테스트가 가능하니 수정하도록한다.

##### Calculator_tests(done 호출 추가)
```javascript
describe('Calculator',()=>{
    let myApp;
    const dummyArray = [
        1,2,3,4,5,6,7,8,9,10
    ];
    const dummyNdepthArray = [
        1,2,3,4,5,6,7,8,9,10,
        [
            1,2,3,4,5,6,7,8,9,10,
            [
                1,2,3,4,5,6,7,8,9,10
            ]
        ]
    ];
    const badArguments = [
        1,'a',undefined,3,[],true,function () {console.log('a');}
    ];
    beforeEach(()=>{
        myApp = new MyApp();
        myApp.setCalculator(new Calculator());
    });

    describe('Calculator.add()',()=>{

        it('integer parameters add',(done)=>{
            console.log('before');
            const result= myApp.calculator.addition(1,2,3);
            result.then((value)=>{
                console.log(value+':'+(value === 6));
                expect(value).toBe(6);
            }).then(done);
            console.log('after');
        });
        it('integer parameters | ArrayParameter add',(done)=>{
            console.log('before');
            const result= myApp.calculator.addition(1,2,dummyArray);
            result.then((value)=>{
                console.log(value+':'+(value === 58));
                expect(value).toBe(58);
            }).then(done);
            console.log('after');
        });
        it('N depth ArrayParameter add',(done)=>{
            console.log('before');
            const result= myApp.calculator.addition(1,2,dummyNdepthArray);
            result.then((value)=>{
                console.log(value+':'+(value === 168));
                expect(value).toBe(168);
            }).then(done);
            console.log('after');
        });
        it('Other type add',(done)=>{
            console.log('before');
            const result = myApp.calculator.addition(badArguments);
            result.then((value)=>{

            }).catch((e)=>{
                console.log(e);
                expect(e).toThrowError(new Error('The argument is invalid.'));
            }).then(done);
            console.log('after');
        });
    });
});
```

우리가 작성한 비동기함수의 처리가 완료된 후 done 을 호출하도록 하였다.

이제 테스트를 다시 실행해본다.

##### Calculator.html done 추가 후 개발자도구 콘솔화면 및 테스트결과)
![Alt text](/assets/javascript_tdd_image/ex5/index12.png)

보면 테스트 결과와 로그상의 변화가 보일것이다.

이전에는 before, after 1세트가 출력되고 promise 의 then or catch 값이 출력 되었다.

지금은 before, after, promise 결정값이 1세트로 묶여서 정상 출력된다.

그리고 테스트 결과 또한 정상적으로 오류를 발생시키고있다.

이제 'integer parameters | ArrayParameter add' 테스트와 'N depth ArrayParameter add' 테스트를 성공시켜본다.

일단 Array 테스트가 실패하는것은 재귀 호출하는 부분에서 문제가 있다.
```javascript
else if(Array.isArray(value)){
    result += Calculator.prototype.addition(...value);
}
```
addition 은 ```return Promise.resolve(result);``` 로 처리 결과값을 응답한다.
헌데 매개변수가 Array 일때 처리하는 부분에서 result 에 응답받은 Promise 를 result 에 더하고 있다.

그래서 아래처럼 수정해본다.

```javascript
else if(Array.isArray(value)){
    Calculator.prototype.addition(...value).then((value)=>{
        console.log(value);
        return result += value;
    });
}
```

테스트를 실행해본다.

##### Calculator.html
![Alt text](/assets/javascript_tdd_image/ex5/index13.png)

하지만 테스트는 여전히 실패이다. 대신 Promise 객체가 더해진게 아니라 3까지만 더해진 상태이다.

조금 생각해본다.

1,2 매개변수가 더해진 결과가 먼저
```javascript
Promise.resolve(result)
```
위 코드를 통해 resolve 로 반환된다.

그전까지 Array 를 매개변수로한 addition 호출은 끝나지 않는다.

이 전체 연산에 대해서 운명을 결정할 Promise 로의 변경을 하도록한다.

##### Calculator
```javascript
Calculator.prototype.addition = (...args)=>{
    return new Promise((resolve,reject)=>{
        let result = 0;
        let isContainArray = false;
        args.forEach((value)=>{
            if(typeof value === 'number'){
                result += value;
            } else if(Array.isArray(value)){
                isContainArray = true;
                Calculator.prototype.addition(...value).then((value)=>{
                    result += value;
                    resolve(result);
                }).catch((e)=>{
                    reject(e);
                });
            } else{
               reject(new Error('The argument is invalid.'));
            }
        });
        if(!isContainArray) {
            resolve(result);
        }
    });
};
```

이후 테스트를 실행해본다.

##### Calculator.html
![Alt text](/assets/javascript_tdd_image/ex5/index14.png)

'Other type add' 테스트를 제외하고 통과한다.

여기서 왜 실패할까?

jasmine 의 toThrowError 에 그 이유가 있다.

toThrowError 의 인자로 들어가는 에러는 에러의 type 이  들어간다.

혹은 에러의 type, 메시지 등이 들어갈 수 있다.

또한 throw 를 해줘야한다.(reject 이 아니다.)

그렇기에 지금 상황에서 맞는 함수가 아니다.

굳이 toThrowError 를 쓰겠다면 reject 으로 전달받은 e 를 throw 하는 콜백을 하나 더 작성해야한다.

우리는 reject 이 되었는지 그리고 정상적으로 Error 가 전달되는지가 중요하니 테스트 API 를 수정하도록한다.

##### Calculator_tests
```javascript
it('Other type add',(done)=>{
    const result = myApp.calculator.addition(badArguments);
    result.then((value)=>{

    }).catch((e)=>{
        expect(e).toEqual(new Error('The argument is invalid.'));
    }).then(done);
});
```

테스트를 실행해본다.

##### Calculator.html
![Alt text](/assets/javascript_tdd_image/ex5/index15.png)

모든 테스트는 성공한다.

addition 에 대해서 테스트는 완료 되었다.

이런식으로 subtraction, multiplication, division 등을 테스트를 작성하고 구현해나가면 된다.

### **주의할점**

- 테스트가 모든상황에서 동작한다고 보장해주지 않는다는 것(본인이 작성한 테스트케이스 내에서의 보장).
- 위 내용이 보장되려면 테스트프레임워크에서 제공하는 API 에 대해서 빠삭해야한다는 것.
- 테스트가 성공하였더라도 버그가 발생하면 내 테스트들을 하나하나 뜯어보며 빠진게 없나 확인할 것.


SaveFunc 은 Array, map 등을 정리하며 구현해보도록 한다.

다음 포스팅의 내용은 Array 에 대해서 정리한다.

[Javascript callback-1]:https://kishe89.github.io/javascript/2018/02/11/javascript-callback-1.html
[Javascript callback-2]:https://kishe89.github.io/javascript/2018/02/11/javascript-callback-2.html

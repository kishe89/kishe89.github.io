---
layout: post
title:  "Javascript Aspect Toolkit-2"
date:   2018-02-05 19:24:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Posts
---

AOP 에 대한 내용을 하다가 커뮤니티에서 논쟁이 된 내용을 이야기하느라 못한 이야기를 적는다.
[AOP.js]에서 레파지토리를 클론한다. 혹은 그냥 다운받는다.

##### AOP.js
```javascript
// Created by Fredrik Appelberg: http://fredrik.appelberg.me/2010/05/07/aop-js.html
// Modified to support prototypes by Dave Clayton
Aop = {
  // Apply around advice to all matching functions in the given namespaces
  around: function(pointcut, advice, namespaces) {
    // if no namespaces are supplied, use a trick to determine the global ns
    if (namespaces == undefined || namespaces.length == 0)
      namespaces = [ (function(){return this;}).call() ];
    // loop over all namespaces
    for(var i in namespaces) {
      var ns = namespaces[i];
      for(var member in ns) {
        if(typeof ns[member] == 'function' && member.match(pointcut)) {
          (function(fn, fnName, ns) {
             // replace the member fn slot with a wrapper which calls
             // the 'advice' Function
             ns[fnName] = function() {
               return advice.call(this, { fn: fn,
                                          fnName: fnName,
                                          arguments: arguments });
             };
           })(ns[member], member, ns);
        }
      }
    }
  },

  next: function(f) {
    return f.fn.apply(this, f.arguments);
  }
};

Aop.before = function(pointcut, advice, namespaces) {
  Aop.around(pointcut,
             function(f) {
               advice.apply(this, f.arguments);
               return Aop.next.call(this, f);
             },
             namespaces);
};

Aop.after = function(pointcut, advice, namespaces) {
  Aop.around(pointcut,
             function(f) {
               var ret = Aop.next.call(this, f);
               advice.apply(this, f.arguments);
               return ret;
             },
             namespaces);
};

module.exports = Aop;
```

|용어|의미|
|---|---|
|Advice|배포할 코드 조각|
|Aspect|Advice 가 처리할 문제|
|cross-cutting concern|Aspect 와 동일|
|Target|부가기능을 부여할 대상으로 핵심기능이 담긴 클래스이거나 추가적인 부가기능을 제공할 프록시 오브젝트 일 수 있다|
|Join Point|Advice 가 적용될 위치. 타깃 오브젝트가 구현한 인터페이스의 모든 메서드가 조인 포인트가 된다.|
|Point Cut|Join Point 를 선별하는 기능을 정의한 모듈|
|Proxy|클라이언트와 타깃 사이에 존재하면서 부가기능을 제공하는 오브젝트. 클라이언트는 타깃을 요청하지만, 클라이언트에게는 DI를 통해 타깃 대신 프록시가 주입된다. 클라이언트의 메소드 호출을 대신 받아서 타깃에게 위임하며, 그 과정에서 부가기능을 부여한다. 스프링 AOP는 프록시를 이용한다.|
|Advisor|포인트컷과 어드바이스를 하나씩 갖고 있는 오브젝트. AOP의 가장 기본이 되는 모듈이다. 스프링은 자동 프록시 생성기가 어드바이저 단위로 검색해서 AOP를 적용한다.|

출처 : [AOP(Aspect Oriented Programming)]

```
자바스크립트 패턴과 테스트
길벗출판사,(지은이) 래리 스펜서, 세스 리처즈 ,(옮긴이) 이일웅
```

AOP.js 를 보면 주어진 namespace 를 순회하며 Advice 를 적용할 곳을 찾고 적용한다.
우리가 의존성을 주입한 코드들은 모두 실행된다. 언제 실행되냐에 대해서 결정하는 것이 AOP 의 핵심이다.

책에서는 이를 분석하는 도구로 TDD 를 이용하는 과정을 설명한다.

일단 책에 코드는 ES 를 사용하지 않았다. 그래서 ES 와 섞어 짜고 있는 부분에서 주의할 점을 먼저 이야기한다.
일단 Arrow function 은 생성자에서 사용하지 못한다. 구문에러가 발생할 것이다.
그리고 책에서는 arguments 를 이용하여 인자를 조작하는데 Arrow function 을 이용하게 되면 arguments 를 제어하는 다른 방법을 제공하므로 arguments 를 사용하게 되면 undefined 일것이다.

그 외의 부분은 Arrow function 을 이용할 것이다.

##### AOP_02.js
```javascript
Aop = {
    around:function(fnName, advice, fnObj){
        // Done
        let originalFn = fnObj[fnName];
        fnObj[fnName] =  function() {
            let targetContext = {};
            return advice.call(targetContext,{fn:originalFn, args:arguments});
        };
    }
};
```
##### AOP_tests_02.js
```javascript
describe('Aop',()=>{

    let argPassingAdvice; // 타깃에 인자를 전달할 어드바이스
    let argsToTarget; // targetObj.targetFn 에 전달할 인자들
    let targetObj;
    let executionPoints;
    let targetFnReturn = 123;
    beforeEach(()=>{
        targetObj = {
            targetFn:function(){
                executionPoints.push('targetFn');
                argsToTarget = Array.prototype.slice.call(arguments, 0);
                return targetFnReturn;
            }
        };
        executionPoints = [];

        argPassingAdvice = (targetInfo)=>{
            return targetInfo.fn.apply(this, targetInfo.args);
        };
        argsToTarget = [];
    });

    describe('Aop.around(fnName, advice, targetObj)',()=>{
        it('타깃 함수 호출 시 어드바이스를 실행하도록 한다.', ()=>{

            let excuteAdvice = false;
            let advice = ()=>{
                excuteAdvice = true;
            };
            Aop.around('targetFn',advice,targetObj);
            targetObj.targetFn();
            expect(excuteAdvice).toBe(true);
        });
        it('어드바이스가 타깃 호출을 래핑한다.',()=>{
            let wrappingAdvice = (targetInfo)=>{
                executionPoints.push('wrappingAdvice - 처음');
                targetInfo.fn();
                executionPoints.push('wrappingAdvice - 끝');
            };
            Aop.around('targetFn',wrappingAdvice,targetObj);
            targetObj.targetFn();
            expect(executionPoints).toEqual(['wrappingAdvice - 처음','targetFn','wrappingAdvice - 끝']);

        });
        it('마지막 어드바이스가 기존 어드바이스에 대해 실행되는 방식으로 체이닝 할 수 있다.',()=>{
            const adviceFactory = (adviceId)=>{
                return ((targetInfo)=>{
                    executionPoints.push('wrappingAdvice - 처음 '+adviceId);
                    targetInfo.fn();
                    executionPoints.push('wrappingAdvice - 끝 '+adviceId);
                });
            };
            Aop.around('targetFn',adviceFactory('안쪽'), targetObj);
            Aop.around('targetFn',adviceFactory('바깥쪽'), targetObj);
            targetObj.targetFn();
            expect(executionPoints).toEqual([
                'wrappingAdvice - 처음 바깥쪽',
                'wrappingAdvice - 처음 안쪽',
                'targetFn',
                'wrappingAdvice - 끝 안쪽',
                'wrappingAdvice - 끝 바깥쪽'
            ]);
        });
        it('어드바이스에서 타깃으로 일반 인자를 넘길 수 있다',()=>{

            Aop.around('targetFn',argPassingAdvice,targetObj);
            targetObj.targetFn('a', 'b');
            expect(argsToTarget).toEqual(['a','b']);
        });
        it('타깃의 반환값도 어드바이스에서 참조 할 수 있다.',()=>{

            Aop.around('targetFn', argPassingAdvice, targetObj);
            const returnedValue = targetObj.targetFn();
            expect(returnedValue).toBe(targetFnReturn);
        });
    });

});
```

실제 모듈에는 module.exports 로 commonjs 스타일로도 모듈을 추출하고 있다.
일단은 순서대로 위 테스트를 통과하도록 짜본 결과이다. 책의 코드들이 앞에서와 마찬가지로 작동하지 않는 코드들이 있다. 읽을 때 참고해야할듯 하다.

각 테스트별 수행 작업은 아래 리스트를 참고한다.

- **타깃 함수 호출 시 어드바이스를 실행하도록 한다.**

    - ```javascript
      let targetObj;
      let executionPoints;
      ```
      ```javascript
      beforeEach(()=>{
              targetObj = {
                  targetFn:function(){
                      executionPoints.push('targetFn');
                  }
              };
              executionPoints = [];
          });
      ```
      ```javascript
       it('타깃 함수 호출 시 어드바이스를 실행하도록 한다.', ()=>{

                   let excuteAdvice = false;
                   let advice = ()=>{
                       excuteAdvice = true;
                   };
                   Aop.around('targetFn',advice,targetObj);
                   targetObj.targetFn();
                   expect(excuteAdvice).toBe(true);
               });
      ```
      일단 외부에서 Advice 를 주입할 PointCut 에 해당하는 함수 이름을 TargetFn 으로 한다.
      그리고 타깃 객체를 하나 초기화 한다.

      그리고 실행 여부를 확인할 boolean 값을 가지는 변수를 하나 생성한다.
      실행 여부만 확인하면 되니 간단하게 실행되면 excuteAdvice 를 true 로 변경해주는 Advice 를 작성한다.
      그리고 AOP 는 아래와 같이 작성한다.
      ```javascript
      Aop = {
        around: function(fnName, advice, fnObj) {
          fnObj[fnName] = advice;
        }
      };
      ```
      타겟 오브젝트의 targetFn 을 제공된 advice 로 변경하고 테스트에서는 변경된 targetFn 을 호출하게된다.
      그러므로 excuteAdvice 는 true 가 된다.
- **어드바이스가 타깃 호출을 래핑한다.**

    - ```javascript
      Aop = {
        around: function(fnName, advice, fnObj) {
          var originalFn = fnObj[fnName];
          fnObj[fnName] = function () {
            var targetContext = {};
            advice.call(targetContext, {fn:originalFn});
          };
        }
      };
      ```

      ```javascript
      it('어드바이스가 타깃 호출을 래핑한다.',()=>{
                  let wrappingAdvice = (targetInfo)=>{
                      executionPoints.push('wrappingAdvice - 처음');
                      targetInfo.fn();
                      executionPoints.push('wrappingAdvice - 끝');
                  };
                  Aop.around('targetFn',wrappingAdvice,targetObj);
                  targetObj.targetFn();
                  expect(executionPoints).toEqual(['wrappingAdvice - 처음','targetFn','wrappingAdvice - 끝']);

              });
      ```
      전달된 advice 의 실행전에 targetObj 의 원래 함수를 저장하고 advice 의 호출을 call 로 인자로 실행 컨텍스트와 fn 에 앞에서 저장한 originalFN 을 가지는 Object 를 전달한다.
      advice 로 전달된 wrappingAdvice 의 targetInfo 에 {fn:originalFn} 이 전달되고 이를 targetInfo 로 받아서 실행하여 originalFn 을 래핑하는 wrappingAdvice 가 정상적으로 실행된다.
- **마지막 어드바이스가 기존 어드바이스에 대해 실행되는 방식으로 체이닝 할 수 있다.**

    - ```javascript
      it('마지막 어드바이스가 기존 어드바이스에 대해 실행되는 방식으로 체이닝 할 수 있다.',()=>{
                  const adviceFactory = (adviceId)=>{
                      return ((targetInfo)=>{
                          executionPoints.push('wrappingAdvice - 처음 '+adviceId);
                          targetInfo.fn();
                          executionPoints.push('wrappingAdvice - 끝 '+adviceId);
                      });
                  };
                  Aop.around('targetFn',adviceFactory('안쪽'), targetObj);
                  Aop.around('targetFn',adviceFactory('바깥쪽'), targetObj);
                  targetObj.targetFn();
                  expect(executionPoints).toEqual([
                      'wrappingAdvice - 처음 바깥쪽',
                      'wrappingAdvice - 처음 안쪽',
                      'targetFn',
                      'wrappingAdvice - 끝 안쪽',
                      'wrappingAdvice - 끝 바깥쪽'
                  ]);
              });
      ```
      위 **어드바이스가 타깃 호출을 래핑한다.** 와 Aop 코드는 같다.

      advice 를 여러개 제공할거기 때문에 advice 를 제공할 adviceFactory 를 만들었다.
      adviceFactory 는 인자로 adviceId 를 전달받고 나머지는 이전에 advice 와 똑같다.

      ```javascript
      {
         targetFn:function(){
            executionPoints.push('targetFn');
         }
      };
      ```

      targetObj 는 처음에 위와 같은 targetFn 을 가지는 Object 이다.
      advice 를 주입하는 Aop.around(함수이름, 어드바이스, 오브젝트) 를 통해 처음으로
      ```javascript
      Aop.around('targetFn',adviceFactory('안쪽'), targetObj);
      ```
      를 호출하게 되면 targetObj 는 아래처럼 제공된 advice 로 변경이 되게된다.
      ##### adviceId = '안쪽' 일때의 targetObj.targetFn()
      ```javascript
      (targetInfo)=>{
          executionPoints.push('wrappingAdvice - 처음 '+adviceId);
          //targetInfo.fn(); 은
          //function(){
          //    executionPoints.push('targetFn');
          //}
          //을 호출
          targetInfo.fn();
          executionPoints.push('wrappingAdvice - 끝 '+adviceId);
      }
      ```
      targetInfo 는 위에서 설명 했듯이 .call(this, arg1,arg2,...) 으로 인해
      targetObj 의 원래의 targetFn 이 된다. 그리고 나서 다시한번 adviceId 를 변경한 advice 를 전달하면 최종적으로 아래와 같이 실행된다.
      ```javascript
      (targetInfo)=>{
          executionPoints.push('wrappingAdvice - 처음 '+adviceId);
          //targetInfo.fn(); 은
          //(targetInfo)=>{
          //    executionPoints.push('wrappingAdvice - 처음 '+adviceId);
          //    //targetInfo.fn(); 은
          //    //function(){
          //    //    executionPoints.push('targetFn');
          //    //};
          //    //을 호출
          //    targetInfo.fn();
          //    executionPoints.push('wrappingAdvice - 끝 '+adviceId);
          //};
          //을 호출
          targetInfo.fn();
          executionPoints.push('wrappingAdvice - 끝 '+adviceId);
      }
      ```
      약간 복잡해보이지만 javascript 의 함수 호출 방법들은 함수의 체이닝을 통해서 다양한 기능으로 확장 가능하다.
- **어드바이스에서 타깃으로 일반 인자를 넘길 수 있다**

    - 위까지 진행하면서 기존 함수를 wrapping 할 수 있게 되었다. 이제 advice 에서 타깃 오브젝트로 인자를 넘기는 것을 진행해본다.
      javascript 는 파라미터들을 (xx,xxx,xxxx,...) 으로 전달 받을 수 있는데 이 방법을 제외하고도 arguments 라는 예약어를 통해 전달받을 수 있다(Arrow function 에서는 불가 - [나머지 매개변수]로 처리).
      아래 테스트를 통과하는 advice 를 작성해본다.
      ```javascript
      it('어드바이스에서 타깃으로 일반 인자를 넘길 수 있다',()=>{

          Aop.around('targetFn',argPassingAdvice,targetObj);
          targetObj.targetFn('a', 'b');
          expect(argsToTarget).toEqual(['a','b']);
      });
      ```
      argPassingAdvice 는 targetObj 의 targetFn 에 주입되어서 인자로 'a','b' 를 받았을 때 인자를 전달해야하는 기능을 가진다.
      ```javascript
      argPassingAdvice = (targetInfo)=>{
          return targetInfo.fn.apply(this, targetInfo.args);
      };
      ```
      전달받은 targetInfo 는 fn : original function, args : arguments 를 가지는 객체이고
      이를 처리하기 위해 original function 은
      ```javascript
      targetObj = {
         targetFn:function(){
             executionPoints.push('targetFn');
             argsToTarget = Array.prototype.slice.call(arguments, 0);
         }
      };
      ```
      와 같이 구성한다. 전달 받은 파라미터들을 잘라서 argsToTarget 에 전달하게 된다.
      **function.call(this,arg1,arg2,...) 은 목록을 받고 function.apply(this,[arg1,arg2,...]) 는 array 를 받는다.**
      테스트를 돌려보면 정상적으로 통과하는 것을 볼 수 있다.

- **타깃의 반환값도 어드바이스에서 참조 할 수 있다.**

    - 지금까지는 반환값에 대한 처리가 없었다. 함수는 기본적으로 어떤 입력에대해 출력을 내놓는걸 이른다.
      꼭 전달할 필요가 없을지라도 명시적으로 처리해주는 것이 좋다.
      그리고 반환값을 통해서 굳이 함수 내부의 값에 대해 신경을 안쓸 수 있으므로 없을 이유가 없다.
      일단 반환값을 확인할 테스트를 작성한다.
      ```javascript
      let targetFnReturn = 123;
      ```
      ```javascript
      it('타깃의 반환값도 어드바이스에서 참조 할 수 있다.',()=>{

          Aop.around('targetFn', argPassingAdvice, targetObj);
          const returnedValue = targetObj.targetFn();
          console.log(returnedValue);
          expect(returnedValue).toBe(targetFnReturn);
      });
      ```
      아직까진 targetObj.targetFn() 을 호출할 때 return 값이 없으니 테스트는 실패할 것이다.
      targetObj 에 targetFnReturn 을 return 하도록 수정하고 다시 테스트해본다.
      ```javascript
      targetObj = {
         targetFn:function(){
            executionPoints.push('targetFn');
            argsToTarget = Array.prototype.slice.call(arguments, 0);
            return targetFnReturn;
         }
      };
      ```
      실패한다. 이유는 제공된 advice 의 호출시 해당 함수가 호출되어 return 하지만 around 는 return 을 안하기 때문이다.
      around 에 advice.call 을 return 해주도록 수정한다.
      ```javascript
      Aop = {
          around:function(fnName, advice, fnObj){
              // Done
              let originalFn = fnObj[fnName];
              fnObj[fnName] =  function() {
                  let targetContext = {};
                  return advice.call(targetContext,{fn:originalFn, args:arguments});
              };
          }
      };
      ```
      이제 다시 테스트를 실행해보면 정상적으로 성공하는 것을 볼 수 있다. 함수가 체이닝 되었기때문에 가장 외부 함수의 호출에서도 return 을 해주어야한다.
      이제 반환값에 대한 접근도 가능해졌다.

- **타깃의 반환값도 어드바이스에서 참조 할 수 있다.**

    - javascript 함수의 호출방법들을 이야기 하면서 함수의 실행 콘텍스트를 변경할 수 있다고 이야기했다.
      이는 미리 정의된 함수를 어느 객체에서도 사용가능하다는 장점이 있으면서도 예기치 못한 동작을 할 수 있는 가능성이 생긴다.
      타깃 함수가 해당 객체(전달된)의 컨텍스트에서 실행되는지와 전달된 advice 가 타깃의 컨텍스트에서 실행되는지를 보는 테스트를 작성한다.
      ```javascript
      it('타깃함수를 해당 객체의 콘텍스트에서 실행한다.',()=>{

          let Target = function(){
          const self = this;
          this.targetFn = ()=>{
                  expect(this).toBe(self);
              };
          };
          let TargetInstance = new Target();
          let spyOnInstance = spyOn(TargetInstance,'targetFn').and.callThrough();
          Aop.around('targetFn', argPassingAdvice, targetObj);
          TargetInstance.targetFn();
          expect(spyOnInstance).toHaveBeenCalled();
      });
      it('어드바이스를 타깃의 콘텍스트에서 실행한다.',()=>{
          let advice = function(){
              expect(this).toBe(targetObj);
          }
          Aop.around('targetFn', advice, targetObj);
          targetObj.targetFn();
      });
      ```
      일단 첫번째 테스트는 성공하는 것과 같이 보인다. 두번째 테스트는 실패한다.
      실패 사유를 보면 advice 의 실행 컨텍스트가 {} 이란다.
      ![Alt text](/assets/javascript_tdd_image/ex2/index1.png)

      이를 해결하려면 이전에 사용하던 context 를 지우고 this 로 대체한다(Arrow function 에서는 this 는 감싸고 있는 객체이며 call,apply 등에 this 를 전달해도 무시됨).
      ```javascript
      Aop = {
          around:function(fnName, advice, fnObj){
              // Done
              let originalFn = fnObj[fnName];
              fnObj[fnName] =  function() {
                  return advice.call(this,{fn:originalFn, args:arguments});
              };
          }
      };
      ```
      테스트를 돌려보면 아래처럼 모두 성공할 것이다.
      ![Alt text](/assets/javascript_tdd_image/ex2/index2.png)

기본적인 advice 의 체인에 대한 기능 테스트는 어느정도 완료 된듯하다. 하지만 우리가 작성하던 것중 advice 로 장식된 함수(decorated function) 을 호출하려면
```javascript
targetInfo.fn.apply(this, targetInfo.args);
```
와 같이 호출해줘야 했다. 이기능은 분명히 Aop Toolkit 에서 제공해야할 기능인데 외부에 나와 있다. 이를 내부로 캡슐화 하도록한다.
작성하는 과정은 around 를 작성한것과 같다. 차근차근 진행해본다.
##### Aop.next(targetInfo) test
```javascript
describe('Aop',()=>{

    let argPassingAdvice; // 타깃에 인자를 전달할 어드바이스
    let argsToTarget; // targetObj.targetFn 에 전달할 인자들
    let targetObj;
    let executionPoints;
    let targetFnReturn = 123;
    let Target = function(){
        const self = this;
        this.targetFn = ()=>{
            expect(this).toBe(self);
        };
    };
    beforeEach(()=>{
        targetObj = {
            targetFn:function(){
                executionPoints.push('targetFn');
                argsToTarget = Array.prototype.slice.call(arguments, 0);
                return targetFnReturn;
            }
        };
        executionPoints = [];

        argPassingAdvice = (targetInfo)=>{
            return targetInfo.fn.apply(this, targetInfo.args);
        };
        argsToTarget = [];
    });

    describe('Aop.around(fnName, advice, targetObj)',()=>{
        it('타깃 함수 호출 시 어드바이스를 실행하도록 한다.', ()=>{

            let excuteAdvice = false;
            let advice = ()=>{
                excuteAdvice = true;
            };
            Aop.around('targetFn',advice,targetObj);
            targetObj.targetFn();
            expect(excuteAdvice).toBe(true);
        });
        it('어드바이스가 타깃 호출을 래핑한다.',()=>{
            let wrappingAdvice = (targetInfo)=>{
                executionPoints.push('wrappingAdvice - 처음');
                targetInfo.fn();
                executionPoints.push('wrappingAdvice - 끝');
            };
            Aop.around('targetFn',wrappingAdvice,targetObj);
            targetObj.targetFn();
            expect(executionPoints).toEqual(['wrappingAdvice - 처음','targetFn','wrappingAdvice - 끝']);

        });
        it('마지막 어드바이스가 기존 어드바이스에 대해 실행되는 방식으로 체이닝 할 수 있다.',()=>{
            const adviceFactory = (adviceId)=>{
                return ((targetInfo)=>{
                    executionPoints.push('wrappingAdvice - 처음 '+adviceId);
                    targetInfo.fn();
                    executionPoints.push('wrappingAdvice - 끝 '+adviceId);
                });
            };
            Aop.around('targetFn',adviceFactory('안쪽'), targetObj);
            Aop.around('targetFn',adviceFactory('바깥쪽'), targetObj);
            targetObj.targetFn();
            expect(executionPoints).toEqual([
                'wrappingAdvice - 처음 바깥쪽',
                'wrappingAdvice - 처음 안쪽',
                'targetFn',
                'wrappingAdvice - 끝 안쪽',
                'wrappingAdvice - 끝 바깥쪽'
            ]);
        });
        it('어드바이스에서 타깃으로 일반 인자를 넘길 수 있다',()=>{

            Aop.around('targetFn',argPassingAdvice,targetObj);
            targetObj.targetFn('a', 'b');
            expect(argsToTarget).toEqual(['a','b']);
        });
        it('타깃의 반환값도 어드바이스에서 참조 할 수 있다.',()=>{

            Aop.around('targetFn', argPassingAdvice, targetObj);
            const returnedValue = targetObj.targetFn();
            console.log(returnedValue);
            expect(returnedValue).toBe(targetFnReturn);
        });
        it('타깃함수를 해당 객체의 콘텍스트에서 실행한다.',()=>{


            let TargetInstance = new Target();
            let spyOnInstance = spyOn(TargetInstance,'targetFn').and.callThrough();
            Aop.around('targetFn', argPassingAdvice, targetObj);
            TargetInstance.targetFn();
            expect(spyOnInstance).toHaveBeenCalled();
        });
        it('어드바이스를 타깃의 콘텍스트에서 실행한다.',()=>{
            let advice = function(){
                expect(this).toBe(targetObj);
            }
            Aop.around('targetFn', advice, targetObj);
            targetObj.targetFn();
        });
    });
    describe('Aop.next(targetInfo)',()=>{
        let advice = function (targetInfo) {
            return Aop.next.call(this,targetInfo);
        };
        let originalFn;
        beforeEach(function() {
            originalFn = targetObj.targetFn;
            Aop.around('targetFn',advice, targetObj);
        });
        it('targetInfo.fn에 있는 함수를 호출한다', function() {
            targetObj.targetFn();
            expect(executionPoints).toEqual(['targetFn']);
        });
        it('targetInfo.args에 인자를 전달한다', function() {
            targetObj.targetFn('a','b');
            expect(argsToTarget).toEqual(['a','b']);
        });
        it("targetInfo 함수에서 받은 값을 반환한다", function() {
            var ret = targetObj.targetFn();
            expect(ret).toEqual(targetFnReturn);
        });
        it('주어진 콘텍스트에서 타깃 함수를 실행한다', function() {
            var targetInstance = new Target();
            var spyOnInstance = spyOn(targetInstance,'targetFn').and.callThrough();
            Aop.around('targetFn',advice,targetInstance);
            targetInstance.targetFn();
            expect(spyOnInstance).toHaveBeenCalled();
        });
    });
});
```
지금까지 구현한 내용이기에 테스트에서 크게 다른것이 없다. advice 를 argPassingAdvice 에서 하던일을 캡슐화한
next 함수를 targetInfo 를 인자로 호출하고 그에 따른 이전 테스트에서 봤던 인자, 컨텍스트, 반환, 호출 등에 대해 테스트한다.
여기까지가 Aop Toolkit 의 핵심 기능에 대한 테스트에 따른 구현이다. 지금 구현 되어있는 걸로는 최하위 수준의 펑션에만 적용할 수 있는데
이를 단순 함수 이름 문자열이 아니라 정규표현식을 이용하게 되면 여러 포인트에 지정이 가능한데 이를 AOP 에서는 Point cut 이라고 한다.
포스팅의 맨 앞에서 설명한 표를 보면 되겠다. 생각난김에 around 의 인자 이름을 변경하도록 한다.
그리고 advice 의 실행순서를 변경하는 before, after 또한 정의해준다.
##### Aop.js 최종
```javascript
Aop = {
    around:function(pointCut, advice, fnObj){
        // Done
        let originalFn = fnObj[pointCut];
        fnObj[pointCut] =  function() {
            return advice.call(this,{fn:originalFn, args:arguments});
        };
    },
    next:function (targetInfo) {
        return targetInfo.fn.apply(this, targetInfo.args);
    },
    before:function(pointCut, advice, fnObj) {
        Aop.around(pointCut,
            function (targetInfo) {
                advice.apply(this, targetInfo.args);
                return Aop.next(targetInfo);
            },
            fnObj);
    },
    after:function(pointCut, advice, fnObj) {
        Aop.around(pointCut,
            function(targetInfo) {
                let ret = Aop.next(targetInfo);
                advice.apply(this, targetInfo.args);
                return ret;
            },
            fnObj);
    }
};
```
##### Aop_tests.js 최종
```javascript
describe('Aop',()=>{

    let argPassingAdvice; // 타깃에 인자를 전달할 어드바이스
    let argsToTarget; // targetObj.targetFn 에 전달할 인자들
    let targetObj;
    let executionPoints;
    let targetFnReturn = 123;
    let Target = function(){
        const self = this;
        this.targetFn = ()=>{
            expect(this).toBe(self);
        };
    };
    beforeEach(()=>{
        targetObj = {
            targetFn:function(){
                executionPoints.push('targetFn');
                argsToTarget = Array.prototype.slice.call(arguments, 0);
                return targetFnReturn;
            }
        };
        executionPoints = [];

        argPassingAdvice = (targetInfo)=>{
            return targetInfo.fn.apply(this, targetInfo.args);
        };
        argsToTarget = [];
    });

    describe('Aop.around(fnName, advice, targetObj)',()=>{
        it('타깃 함수 호출 시 어드바이스를 실행하도록 한다.', ()=>{

            let excuteAdvice = false;
            let advice = ()=>{
                excuteAdvice = true;
            };
            Aop.around('targetFn',advice,targetObj);
            targetObj.targetFn();
            expect(excuteAdvice).toBe(true);
        });
        it('어드바이스가 타깃 호출을 래핑한다.',()=>{
            let wrappingAdvice = (targetInfo)=>{
                executionPoints.push('wrappingAdvice - 처음');
                targetInfo.fn();
                executionPoints.push('wrappingAdvice - 끝');
            };
            Aop.around('targetFn',wrappingAdvice,targetObj);
            targetObj.targetFn();
            expect(executionPoints).toEqual(['wrappingAdvice - 처음','targetFn','wrappingAdvice - 끝']);

        });
        it('마지막 어드바이스가 기존 어드바이스에 대해 실행되는 방식으로 체이닝 할 수 있다.',()=>{
            const adviceFactory = (adviceId)=>{
                return ((targetInfo)=>{
                    executionPoints.push('wrappingAdvice - 처음 '+adviceId);
                    targetInfo.fn();
                    executionPoints.push('wrappingAdvice - 끝 '+adviceId);
                });
            };
            Aop.around('targetFn',adviceFactory('안쪽'), targetObj);
            Aop.around('targetFn',adviceFactory('바깥쪽'), targetObj);
            targetObj.targetFn();
            expect(executionPoints).toEqual([
                'wrappingAdvice - 처음 바깥쪽',
                'wrappingAdvice - 처음 안쪽',
                'targetFn',
                'wrappingAdvice - 끝 안쪽',
                'wrappingAdvice - 끝 바깥쪽'
            ]);
        });
        it('어드바이스에서 타깃으로 일반 인자를 넘길 수 있다',()=>{

            Aop.around('targetFn',argPassingAdvice,targetObj);
            targetObj.targetFn('a', 'b');
            expect(argsToTarget).toEqual(['a','b']);
        });
        it('타깃의 반환값도 어드바이스에서 참조 할 수 있다.',()=>{

            Aop.around('targetFn', argPassingAdvice, targetObj);
            const returnedValue = targetObj.targetFn();
            console.log(returnedValue);
            expect(returnedValue).toBe(targetFnReturn);
        });
        it('타깃함수를 해당 객체의 콘텍스트에서 실행한다.',()=>{


            let TargetInstance = new Target();
            let spyOnInstance = spyOn(TargetInstance,'targetFn').and.callThrough();
            Aop.around('targetFn', argPassingAdvice, targetObj);
            TargetInstance.targetFn();
            expect(spyOnInstance).toHaveBeenCalled();
        });
        it('어드바이스를 타깃의 콘텍스트에서 실행한다.',()=>{
            let advice = function(){
                expect(this).toBe(targetObj);
            }
            Aop.around('targetFn', advice, targetObj);
            targetObj.targetFn();
        });
    });
    describe('Aop.next(targetInfo)',()=>{
        let advice = function (targetInfo) {
            return Aop.next.call(this,targetInfo);
        };
        let originalFn;
        beforeEach(function() {
            originalFn = targetObj.targetFn;
            Aop.around('targetFn',advice, targetObj);
        });
        it('targetInfo.fn에 있는 함수를 호출한다', function() {
            targetObj.targetFn();
            expect(executionPoints).toEqual(['targetFn']);
        });
        it('targetInfo.args에 인자를 전달한다', function() {
            targetObj.targetFn('a','b');
            expect(argsToTarget).toEqual(['a','b']);
        });
        it("targetInfo 함수에서 받은 값을 반환한다", function() {
            var ret = targetObj.targetFn();
            expect(ret).toEqual(targetFnReturn);
        });
        it('주어진 콘텍스트에서 타깃 함수를 실행한다', function() {
            var targetInstance = new Target();
            var spyOnInstance = spyOn(targetInstance,'targetFn').and.callThrough();
            Aop.around('targetFn',advice,targetInstance);
            targetInstance.targetFn();
            expect(spyOnInstance).toHaveBeenCalled();
        });
    });
    describe('Aop.before(fnName, advice, targetObj)', function () {
        describe('어드바이스가 성공할 경우', function() {

            it('타깃 함수를 호출하면 어드바이스를 타깃 다음에 실행한다', function() {
                let advice = function() {
                    executionPoints.push('successfulAdvice');
                };
                Aop.before('targetFn',advice,targetObj);
                targetObj.targetFn();
                expect(executionPoints).toEqual(['successfulAdvice','targetFn']);
            });

            it('어드바이스에 인자를 전달한다', function() {
                let argsToAdvice;
                let advice = function() {
                    argsToAdvice = Array.prototype.slice.call(arguments,0);
                };
                Aop.before('targetFn',advice,targetObj);
                targetObj.targetFn(11,22,33);
                expect(argsToAdvice).toEqual([11,22,33]);
            });

            it('타깃 함수에 인자를 전달한다', function() {
                Aop.before('targetFn', function() {},targetObj);
                targetObj.targetFn('a','b');
                expect(argsToTarget).toEqual(['a','b']);
            });

            it('마지막 어드바이스를 제일 먼저 실행하는 식으로 체이닝이 가능한다', function() {
                let adviceFactory = function(adviceID) {
                    return (function() {
                        executionPoints.push(adviceID);
                    });
                };
                Aop.before('targetFn',adviceFactory('안쪽'),targetObj);
                Aop.before('targetFn',adviceFactory('바깥쪽'),targetObj);
                targetObj.targetFn();
                expect(executionPoints).toEqual(['바깥쪽','안쪽','targetFn']);
            });

            it("타깃 함수를 호출하면 일반 값을 반환한다", function() {
                Aop.before('targetFn', function() {}, targetObj);
                expect(targetObj.targetFn()).toEqual(targetFnReturn);
            });

            it('어드바이스를 타깃의 콘텍스트에서 실행한다', function() {
                let advice = function() {
                    expect(this).toBe(targetObj);
                };
                Aop.before('targetFn',advice, targetObj);
                targetObj.targetFn();
            });
        });

        describe('어드바이스에서 예외가 발생할 경우', function() {
            let badAdvice = function() {
                executionPoints.push('badAdvice');
                throw new Error('실패!');
            };
            let goodAdvice = function() {
                executionPoints.push('goodAdvice');
            };
            let expectJustBadAdvice = function() {
                try {
                    targetObj.targetFn();
                }
                catch (e) {
                }
                expect(executionPoints).toEqual(['badAdvice']);
            };
            it('다음 어드바이스는 실행되지 않는다', function() {
                Aop.before('targetFn',goodAdvice,targetObj);
                Aop.before('targetFn',badAdvice,targetObj);
                expectJustBadAdvice();
            });
            it('타깃도 실행되지 않는다', function() {
                Aop.before('targetFn',badAdvice,targetObj);
                expectJustBadAdvice();
            });
        });

    });

    describe('Aop.after(fnName, advice, targetObj)', function () {

        describe('타깃이 성공할 경우', function() {
            it('타깃 직후에 실행한다', function() {
                let advice = function() {
                    executionPoints.push('advice');
                };
                Aop.after('targetFn',advice,targetObj);
                targetObj.targetFn();
                expect(executionPoints).toEqual(['targetFn','advice']);
            });
            it("타깃의 인자로 실행한다", function() {
                let argsToAdvice;
                let advice = function() {
                    argsToAdvice = Array.prototype.slice.call(arguments,0);
                };
                Aop.after('targetFn',advice,targetObj);
                targetObj.targetFn(11,22,33);
                expect(argsToAdvice).toEqual([11,22,33]);
            });
            it('타깃의 콘텍스트로 실행한다', function() {
                let advice = function() {
                    expect(this).toBe(targetObj);
                };
                Aop.after('targetFn',advice, targetObj);
                targetObj.targetFn();
            });
            it('타깃의 반환값을 반환한다', function() {
                Aop.after('targetFn', function() {}, targetObj);
                expect(targetObj.targetFn()).toEqual(targetFnReturn);
            });
            it('최초의 어드바이스가 제일 먼저 실행되는 식으로 체이닝이 가능한다', function() {
                let adviceFactory = function(adviceID) {
                    return (function() {
                        executionPoints.push(adviceID);
                    });
                };
                Aop.after('targetFn',adviceFactory('first'),targetObj);
                Aop.after('targetFn',adviceFactory('second'),targetObj);
                targetObj.targetFn();
                expect(executionPoints).toEqual(['targetFn','first','second']);
            });
        });

        describe('타깃에서 예외가 발생할 경우', function() {
            it('실행되지 않는다', function() {
                let executedAdvice = false,
                    badTarget = {
                        badFn : function () {
                            throw new Error('Oops!');
                        }
                    },
                    advice = function() {
                        executedAdvice = true;
                    };

                Aop.after('badFn', advice, badTarget);

                try
                {
                    badTarget.badFn(); // 예외가 발생하지 않으면 테스트는 성공한다.
                }
                catch (e) {}
                expect(executedAdvice).toBe(false);
            });
        });
    });
});
```
##### 최종 테스트 결과화면
![Alt text](/assets/javascript_tdd_image/ex2/index3.png)

책에서 코드 검사 도구들을 추가로 소개하는데 IDE 를 사용중이라면 거의 기본 린트는 지원한다.
javascript 는 이런 도구를 제외하고도 문법 검사를 지원하는 옵션이 있는데 'use strict' 이다.
앞에서 작성한 Aop.js 를 'use strict'(엄격모드) 로 변경해보자.
Aop 변수를 선언하지 않았다고 바로 에러를 띄워줄것이다.
린팅 도구는 각각의 린트 규칙에 따라 경고해준다. 그러므로 사용하려는 스타일의 린트 도구를 사용하면 된다.
대표적으로 Javascript 에는 JsHint,JsLint, ESLint 등이 있다.

다음 포스팅은 Javascript 에서의 prototype 과 클래스 그리고 상속 및 추출에 대해 보도록한다.

[나머지 매개변수]:https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Functions/rest_parameters
[AOP(Aspect Oriented Programming)]:http://blog.naver.com/PostView.nhn?blogId=kbh3983&logNo=220836425242
[AOP.js]:https://github.com/davedx/aop

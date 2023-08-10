const url = window.location.href
console.log(url)
const quizForm = document.getElementById('quiz-form')

$.ajax({
    type: 'GET',
    url: `${url}/data`,
    success: function(response){
        const data = response.data
        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)){
                const quizBox = document.getElementById('quiz-box')
                quizBox.innerHTML += `
                
            <style>
            .text-container {
                text-align: center;
                margin-top: 50px;
            }
            </style>
            <div class="text-container">
                <span  font-weight: bold;">${question}</span>
            </div>
                `
                answers.forEach(answer=> {
                    quizBox.innerHTML += `
                    <style>              
                    .form-control {
                      display: grid;
                      grid-template-columns: 1em auto;
                      gap: 0.5em;
                      margin-top: 10px;
                      box-shadow: #45414223 0 5px 5px;
                      height: auto;
                    }

                    .form-control:focus-within {
                        animation: sparkles 800ms ease-in-out;

                      }
                    .form-control:hover {
                        border-color: #4062F6;
                    }

                      @keyframes sparkles {
                        0%, 10% { opacity: 0; transform: scale(0); }
                        15% {
                            opacity: 1;
                        transform: scale(1.05) ;
                            @include sparkles(0);
                        }
                    }
                      
                    input[type="radio"] {
                      /* Add if not using autoprefixer */
                      -webkit-appearance: none;
                      /* Remove most all native input styles */
                      appearance: none;
                      /* For iOS < 15 */
                      background-color: var(--form-background);
                      /* Not removed via appearance */
                      margin: 0;
                    
                      font: inherit;
                      width: 1.15em;
                      height: 1.15em;
                      border: 1px solid black;
                      border-radius: 50%;
                      transform: translateY(0.2em);
                      display: grid;
                      place-content: center;
                    }
                    
                    input[type="radio"]::before {
                      content: "";
                      width: 0.65em;
                      height: 0.65em;
                      border-radius: 50%;
                      transform: scale(0);
                      transition: 120ms transform ease-in-out;
                      box-shadow: inset 1em 1em black;


                      /* Windows High Contrast Mode */
                      background-color: CanvasText;
                    }
                    
                    input[type="radio"]:checked::before {
                      transform: scale(1);


                    }
                    </style>
                    <div style="margin-bottom: 15px;">
                    <label class="form-control">
                    <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                    ${answer}


                    </label>
                 </div>


                        `
                })
            }
        });
    },
    error: function(error){
        console.log(error)
    }
})



const sendData = ()=> {
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    const csrf = document.getElementsByName('csrfmiddlewaretoken')
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(el=>{
        if(el.checked){
            data[el.name] = el.value 
        } else {
            if(!data[el.name]){
                data[el.name] = null
            }
        }
    })
    $.ajax({
        type: 'POST',
        url: `${url}/save`,
        data: data,
        success: function(response){
            const quizForm = document.getElementById('quiz-form')
            const results = response.results
            console.log(results)
            quizForm.classList.add("not-visible")
           
            results.forEach(res=>{
                const resDiv = document.createElement("div")
                for (const [question, resp] of Object.entries(res)){
                    const scoreBox = document.getElementById('score-box')
                    scoreBox.innerHTML = `
                    <style>
                    
                    .animate-charcter
{
   text-transform: uppercase;
  background-image: linear-gradient(
    -225deg,
    #231557 0%,
    #44107a 29%,
    #ff1361 67%,
    #fff800 100%
  );
  background-size: auto auto;
  background-clip: border-box;
  background-size: 200% auto;
  color: #fff;
  background-clip: text;
  text-fill-color: transparent;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: textclip 2s linear infinite;
  display: inline-block;
      font-size: 10vw;
}


@keyframes textclip {
  to {
    background-position: 200% center;
  }
}
.score{
    text-align: center;
}
.resultText{
    font-size: 2rem;
    font-family: "Poppins", sans-serif;


}
@media only screen and (min-width: 760px) {
    .animate-charcter{
        font-size: 8vw;
    }
  } 
                    </style>
                    <div class="container">
  <div class="row">
    <div class="col-md-12 text-center" style="margin-top: 10px;">
      <h3 class="animate-charcter"> ${response.passed ? 'Congrats! ' : 'Oh no... '}</h3>
    </div>
  </div>
</div>
                    <div class="score">
                    <p class="resultText">Your result is ${response.score.toFixed(2)}%</p>
                    <p> ${response.passed ? 'You have pass the quiz, good job. ' : 'The required score to pass is 100%, please try again later :) '}</p>


                    </div>
`
                    resDiv.innerHTML += question
                    const cls = ['container', 'p-3', 'text-dark', 'h6']
                    resDiv.classList.add(...cls)


                    if (resp == 'not answered') {
                        const nclss = ['border','border-danger', 'rounded','border-3']
                            resDiv.classList.add(...nclss)
                        resDiv.innerHTML += `
                        <div style="color: red; margin-top: 10px;">
                        <b>Not Answered</b>
                        </div>
                        `
                    }
                    else{
                        const answer = resp['answered']
                        const correct = resp['correct_answer']
                        console.log(answer, correct)
                        if(answer == correct){
                            const clss = ['border','border-success', 'rounded','border-3']
                            resDiv.classList.add(...clss)


                            resDiv.innerHTML += `
                            <div style="color: green; margin-top: 10px;">
                            Answered: ${answer}
                            </div>


                            <div style="color: green; margin-top: 2px;">
                            <b>Correct</b>
                            </div>`
                        } else {
                            const wclss = ['border','border-danger', 'rounded','border-3']
                            resDiv.classList.add(...wclss)
                            resDiv.innerHTML += `
                            <div style="color: red; margin-top: 10px;">
                            Answered: ${answer}
                            </div>
                            <div style="color: red; margin-top: 2px;">
                            <b>Wrong</b>
                            </div>`
                            
                        }
                    }
                }
                const resultBox = document.getElementById('result-box')
                resultBox.append(resDiv)
            })
        },
        error: function(error){
            console.log(error)
        }
    })
}


quizForm.addEventListener('submit', e=>{
    e.preventDefault()
    sendData()
})
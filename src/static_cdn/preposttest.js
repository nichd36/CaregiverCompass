const url = window.location.href
console.log(url)
const quizForm = document.getElementById('quiz-form')

$.ajax({
    type: 'GET',
    url: `${url}/data`,
    success: function(response){
        const essay_questions = response.essay_questions;
        const essayBox = document.getElementById('essay_questions');
        console.log("essay");

        essay_questions.forEach((question,index) => {
            essayBox.innerHTML += `
            <div class="essay-question">${question}
            <input style="width=100%" class="essayans" name="${question}" id="essay-answer-${index}" placeholder="Your answer here"></input>
            </div>`;
            console.log(question);
        });

        const data = response.data;
        const quizBox = document.getElementById('mcq');
        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)){
                
                mcqHTML = `
                
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
                    mcqHTML += `
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
                    //   background: linear-gradient(to top right, #6E89FF, #4363EE);
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

                quizBox.innerHTML += mcqHTML;
            }
            // END OF MCQ
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

    const essayAnswer = [...document.getElementsByClassName('essayans')]
    essayAnswer.forEach(ans=>{
        data[`essay_answer_${ans.name}`] = ans.value
    })


// const essayAnswers = document.querySelectorAll('[id^="essay-answer-"]');
//     essayAnswers.forEach((essayAnswer, index) => {
//         data[`essay_answer_${index}`] = essayAnswer.value;
        
//     });
    
    $.ajax({
        type: 'POST',
        url: `${url}/save`,
        data: data,
        
        success: function(response){
            const quizForm = document.getElementById('quiz-form')
            quizForm.classList.add("not-visible")
           
            // results.forEach(res=>{
            //     for (const [question, resp] of Object.entries(res)){
                    const scoreBox = document.getElementById('score-box')
                    scoreBox.innerHTML = `
                    <style>
                    
                    .animate-character
{
   text-transform: uppercase;
  background-image: linear-gradient(
    -225deg,
    #231557 0%,
    #44107a 29%,
    #ff1361 67%,
    #fff800 100%,
    #ff1361 67%,
    #44107a 29%
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
      font-size: 4rem;
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
    font-size: 1rem;
    font-family: "Poppins", sans-serif;


}
                    </style>
                    <div class="container">
  <div class="row">
    <div class="col-md-12 text-center">
      <h5 class="animate-character">${response.passed ? 'DONE! ' : 'Oh no... an error occured'}</h5>
    </div>
  </div>
</div>
                    <div class="score">
                    <p class="resultText">${response.passed ? "Now let's go back to the topics and start our journey in DementiaLearn! 🙌🎉 " : "Seems like you've done the pretest before, your score this time won't be recorded"}</p>
                    </div>`
            //     }
            // })
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
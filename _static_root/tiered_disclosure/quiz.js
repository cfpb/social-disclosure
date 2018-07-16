$(document).ready(function() {
    // This works for multiple questions on a page.
    //  I think I'd need to add css for .quiz_js.selected
    // Currently just tested for a single quiz question per page.
    var quizzes = $("div.quiz_js");

    // Giving labels some selection styling
    $(".controls label").click(function(){
        $(".controls label").removeClass("selected");
        $(this).addClass("selected");
    });

    var checkRequired = function(selected){
        var radios = $("input[type='radio']", quizzes.eq(selected));
        if( $(radios[0]).attr("required") ){
            var checked = false;
            $(radios).each(function(i, radio){
                checked = $(radio).is(':checked') ? true : checked;
            });
//            console.log(checked);
            if( !checked ){
                // This will not submit the form because we have a required
                //  form element that is blank, it will just trigger
                //  the native browser form validation.
                $("nav input[type='submit']").click();
                return false;
            }
        }
        return true;
    }

    var selectQuestion = function(selected, i){
        if(i == quizzes.length){
            $("form").submit();
            return 0;
        }
        quizzes.eq(selected).removeClass("selected");
        selected = i;

        // New selected
        var quiz = quizzes.eq(selected).addClass("selected");
        $(".question", quiz).show();
        $(".answer", quiz).hide();

        // Next Button Click
        $("nav .next").unbind().click(function(){
            if( checkRequired(selected) ){
                selected = selectAnswer(selected);
            }
        });

        return selected;
    }

    var selectAnswer = function(selected){
        console.log(selected)
        var quiz = quizzes.eq(selected);
        // Capture the participant's answer
//        var name = "q" + (selected + 1).toString();
//        console.log(name)
//        var correct = $("input:radio[name='" + name + "']:checked").attr("data-correct");
//        console.log($("input:radio[name='" + name + "']:checked"))
        var correct = $("input:radio[type='radio']:checked", quiz).attr("data-correct");
        console.log(correct)

        // Show what must be shown
        $(".question", quiz).hide();
        $(".answer", quiz).show();
        if(correct == "true"){
            $(".correct", quiz).show()
        } else{
            $(".incorrect", quiz).show()
        }
        // Change Next behavior to view the next question
        $("nav .next").unbind().click(function(){
            selected = selectQuestion(selected, selected + 1)
        });
    }

    // Init
    var selected = selectQuestion(0, 0);
});
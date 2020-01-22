$(document).ready(function () {
    
    // Configurando os módulos de interpolação
    $('.interpolador').each(function(){
        
        console.log("Carregando interpolador... ")
        var elementoPai = this;

        function setFrame(frame){
            console.log("Mostra o frame de nº " + frame + " ...")

            $(elementoPai).find(".interpolador-category.visible img").each(function(index){
                if(index <= frame){
                    $(this).addClass('visible');
                } else {
                    $(this).removeClass('visible');
                }
            });
        }

        function setDirection(direction){
            console.log("Alterando direção para " + direction + "... ");
            
            $(elementoPai).find('.interpolador-category').each(function(){
                let d = $(this).attr('direction');
                if( d === direction){
                    $(this).addClass('visible');
                } else {
                    $(this).removeClass('visible');
                }
            });

            // Exibindo novamente o frame central
            var quantFrames = $(elementoPai).find(".interpolador-category.visible").children('img').length;
            setFrame(quantFrames/2);
            $(elementoPai).find('.controller').val(quantFrames/2);
        }

        $(elementoPai).find('.direction-select').on('change', function(){
            let d = this.value;
            setDirection(d);
        });

        $(elementoPai).find('.controller').on('input', function(){
            let frame = this.value;
            setFrame(frame);
        });

        setDirection('age')
    });
    
    
    
    
    
})


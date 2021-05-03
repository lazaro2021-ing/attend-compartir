function copy() {
    /* Get the text field */
    var copyText = document.getElementById("confirm_copy");
  
    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /* For mobile devices */
  
    /* Copy the text inside the text field */
    document.execCommand("copy");
  
  }


function ver_table(element){

  let group = document.getElementsByName("table_group");
    group.forEach(table => {
        if (table.id == element.value) {
            
                document.getElementById(element.value).style.display = 'block'
        } else {
            document.getElementById(table.id).style.display = 'none';
        
        }
    }
    )
  
}
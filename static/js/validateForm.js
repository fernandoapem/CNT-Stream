function validateForm(){
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    if(username == "username" && password == "password"){
        window.location.href = '/stream'; 
    }
    else
    {
        element = document.getElementById("password-div");
    
        htmlString=`
        <input type="password" class="form-control is-invalid" id="password" aria-describedby="validationServer03Feedback" required>
            <div id="validationServer03Feedback" class="invalid-feedback">
            Incorrect username or password.
        </div>`;
        element.outerHTML = htmlString;
    }
}
% rebase('base.tpl', note=note, error=error)
<div class="box">
<form action="/log_in/", method="POST">
    <div class="field">
        <label class="label">Username</label>
        <div class="control has-icons-left">
            <input class="input" name="username" type="text" placeholder="username">
            <span class="icon is-small is-left">
                <i class="fas fa-user"></i>
            </span>
        </div>
    </div>
    <div class="field">
        <label class="label">Password</label>
        <div class="control has-icons-left">
            <input class="input" name="password" type="password" placeholder="password">
            <span class="icon is-small is-left">
                <i class="fas fa-lock"></i>
            </span>
        </div>
    </div>
    
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link has-background-grey-light">
            Login
            </button>
        </div>
    </div>
</form>
</div>

<div class="box">
<p class="has-text-info">
FOR NEW USERS:</p>
<form action="/register/", method="POST">
    <div class="field">
        <label class="label">Username</label>
        <div class="control has-icons-left">
            <input class="input" name="username" type="text" placeholder="username">
            <span class="icon is-small is-left">
                <i class="fas fa-user"></i>
            </span>
        </div>
    </div>
    <div class="field">
        <label class="label">Password</label>
        <div class="control has-icons-left">
            <input class="input" name="password" type="password" placeholder="password">
            <span class="icon is-small is-left">
                <i class="fas fa-lock"></i>
            </span>
        </div>
    </div>
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link has-background-grey-light">
            Register
            </button>
        </div>
    </div>
</form>
</div>
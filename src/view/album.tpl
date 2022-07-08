% rebase('base.tpl')
<p>{{username}}</p>
<form action="/" method="get">
    <input name = main_page value="Go to main page" type="submit" class="btn btn-outline-primary"/>
</form>
<form method="POST">
    <div class="field is-grouped">
        <div class="control">
            <button class="button is-link">new photo</button>
        </div>
    </div>
</form>

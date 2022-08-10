<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    % if defined("current_page"):
    <title>Memories {{current_page}}</title>
    % else:
    <title>Memories</title>
    % end
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.8.2/css/bulma.min.css">
    <script defer src="https://use.fontawesome.com/releases/v5.3.1/js/all.js"></script>
  </head>
  
  <body>
    <nav class="navbar is-light">
      <div class="container">
        <div class="navbar-brand">
          <span class="navbar-item">
            <span class="icon">
              <i class="fa fa-camera-retro" aria-hidden="true"></i>
            </span>
            
            <strong>Memories</strong>
            % if defined("current_page"): 
            <p>{{current_page}}</p>
            % end
          </span>
        </div>
        <div class="navbar-start">
          % if defined("current_page"):
            <form method="POST" action="/log_out/">
                <button class="is-small is-rounded">
                  ({{account.username}})<br />
                  <p>Log out</p>
                </button>
              </form>
            </form>
            % if current_page != "Home page":
            <a class="navbar-item" href="/main_page/">
              <span class="icon">
                <i class="fa fa-home" aria-hidden="true"></i>
              </span>
            % end
          % end
        </div>
        <div class="navbar-end">
          </div>
          <a class="navbar-item" href="https://github.com/LanaP3/Memories">
            <span class="icon">
              <i class="fab fa-github"></i>
            </span>
          <span>GitHub</span>
          </a>
        </div>
      </div>
    </nav>

    <section class="section">
      {{!base}}
    </section>

    <footer>© 2022, Lana Prijon</footer>
  </body>
</html>
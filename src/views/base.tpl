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
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.5/css/bulma.min.css">
    <script src="https://kit.fontawesome.com/2f90d8839a.js" crossorigin="anonymous"></script>
  </head>
  
  <body>
    <nav class="navbar is-light">
      <div class="container">
        <div class="navbar-brand">
          <span class="navbar-item">
            <span class="icon">
              <i class="fa-solid fa-camera-retro"></i>
            </span>
            <strong>Memories</strong>
          </span>
        </div>
        <div class="navbar-start">
          % if defined("current_page"):
            <form method="POST" action="/log_out/">
                <button class="is-small is-rounded">                  
                  <b>Log out</b><br/>
                  <small>{{account.username}}</small>
                </button>
              </form>
            </form>
            % if current_page != "Home page":
            <a class="navbar-item" href="/main_page/">
              <span class="icon">
                <i class="fa-solid fa-house-chimney"></i>
              </span>
            % end
            % if current_page == "image":
            <a class="navbar-item" href="/album/">
              <span class="icon">
                <i class="fa-regular fa-circle-left"></i>
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

    <section class="section is-dark">
    % if "note":
    <div class="content">
			<div class="subtitle is-size-6">{{note}}</div>
    </div>
    % end
      {{!base}}
    </section>

    <footer>© 2022, Lana Prijon</footer>
  </body>
</html>
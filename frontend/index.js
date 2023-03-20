const bulletin = document.getElementById("bulletin");
const available = document.getElementById("available");
const submitButton = document.getElementById("submit");

const bulletinSortable = Sortable.create(bulletin, {
  group: "shared",
  animation: 150,
});
Sortable.create(available, { group: "shared", animation: 150 });

var current_user;
function onTelegramAuth(user) {
  const loginButton = document.getElementById(
    "telegram-login-dshindov_vote_bot"
  );
  current_user = user;
  loginButton.style.display = "none";
  submitButton.style.display = "block";
}

function submitVote() {
  if (typeof current_user === "undefined") {
    alert("Как ты сюда попал? В любом случае, тебе сначала надо залогиниться.");
    return;
  }
  const data = bulletinSortable.toArray().map((x) => parseInt(x));
  if (data.length === 0) {
    alert("Добавь хотя бы одного кандидата в бюллетень.");
    return;
  }
  const req = {
    user: current_user,
    data,
  };
  fetch("https://dshindov.ru/vote/", {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify(req),
  }).then((response) => {
    if (response.ok) {
      alert("Ваш бюллетень принят в обработку!");
    } else {
      alert(
        "Что-то пошло не так( Возможно проблема с авторизацией, или же вы попытались отправить свой бюллетень дважды. Попробуйте ещё раз или свяжитесь с дшиндовым."
      );
    }
  });
}

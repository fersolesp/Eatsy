// get all the stars
const one = document.getElementById("first");
const two = document.getElementById("second");
const three = document.getElementById("third");
const four = document.getElementById("fourth");
const five = document.getElementById("fifth");
const valoracionMedia = document.getElementById("valoracion_media");

// get the form and csrf token
const form = document.querySelector(".rate-form");
const csrf = document.getElementsByName("csrfmiddlewaretoken");

const handleStarSelect = (size) => {
    const children = form.children;
    for (let i = 0; i < children.length; i++) {
        if (i <= size) {
            children[i].classList.add("checked");
        } else {
            children[i].classList.remove("checked");
        }
    }
};

const handleSelect = (selection) => {
    switch (selection) {
        case "first":
            handleStarSelect(1);
            return;
        case "second":
            handleStarSelect(2);
            return;
        case "third":
            handleStarSelect(3);
            return;
        case "fourth":
            handleStarSelect(4);
            return;
        case "fifth":
            handleStarSelect(5);
            return;
        default:
            handleStarSelect(0);
    }

};

const getNumericValue = (stringValue) => {
    let numericValue;
    if (stringValue === "first") {
        numericValue = 1;
    } else if (stringValue === "second") {
        numericValue = 2;
    } else if (stringValue === "third") {
        numericValue = 3;
    } else if (stringValue === "fourth") {
        numericValue = 4;
    } else if (stringValue === "fifth") {
        numericValue = 5;
    } else {
        numericValue = 0;
    }
    return numericValue;
};

handleStarSelect(valoracionMedia.value);

if (one) {
    const arr = [one, two, three, four, five];

    arr.forEach((item) => item.addEventListener("mouseover", (event) => {
        handleSelect(event.target.id);
    }));

    arr.forEach((item) => item.addEventListener("mouseout", (event) => {
        handleStarSelect(valoracionMedia.value);

    }));

    arr.forEach((item) => item.addEventListener("click", (event) => {
        // value of the rating not numeric
        const val = event.target.id;

        let isSubmit = false;
        form.addEventListener("submit", (e) => {
            e.preventDefault();
            if (isSubmit) {
                return;
            }
            isSubmit = true;
            // picture id
            const id = e.target.id;
            // value of the rating translated into numeric
            const valNum = getNumericValue(val);

            $.ajax({
                type: "POST",
                url: "/product/show/" + id + "/rate",
                data: {
                    "csrfmiddlewaretoken": csrf[0].value,
                    "id": id,
                    "rate": valNum,
                },
                success: function(response) {
                    document.getElementById("msjrating").display = "block";
                    if (response["msj"] === "Ya ha realizado una valoración") {
                        document.getElementById("msjrating").classList.add("msjError");
                    } else {
                        document.getElementById("msjrating").classList.add("msj");
                    }
                    document.getElementById("msjrating").innerHTML = response["msj"];
                    setTimeout(() => {
                        document.getElementById("msjrating").style.display = "none";
                        if (response["msj"] === "Ya ha realizado una valoración") {
                            document.getElementById("msjrating").classList.remove("msjError");
                        } else {
                            document.getElementById("msjrating").classList.remove("msj");
                        }
                    }, 3000);
                }
            });
        });
    }));
}
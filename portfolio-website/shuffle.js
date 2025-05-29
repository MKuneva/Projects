// Generating the header's text
const resolver = {
    resolve: function resolve(options, callback) {
        // The string to resolve
        const resolveString = options.resolveString || options.element.getAttribute('data-target-resolver');
        const combinedOptions = Object.assign({}, options, { resolveString: resolveString });

        function getRandomInteger(min, max) {
            return Math.floor(Math.random() * (max - min + 1)) + min;
        };

        function randomCharacter(characters) {
            return characters[getRandomInteger(0, characters.length - 1)];
        };

        function doRandomiserEffect(options, callback) {
            const characters = options.characters;
            const timeout = options.timeout;
            const element = options.element;
            const partialString = options.partialString;

            let iterations = options.iterations;

            setTimeout(() => {
                if (iterations >= 0) {
                    const nextOptions = Object.assign({}, options, { iterations: iterations - 1 });

                    // Ensures partialString without the random character as the final state.
                    if (iterations === 0) {
                        element.textContent = partialString;
                    } else {
                        // Replaces the last character of partialString with a random character
                        element.textContent = partialString.substring(0, partialString.length - 1) + randomCharacter(characters);
                    }

                    doRandomiserEffect(nextOptions, callback);
                } else if (typeof callback === "function") {
                    callback();
                }
            }, options.timeout);
        };

        function doResolverEffect(options, callback) {
            const resolveString = options.resolveString;
            const characters = options.characters;
            const offset = options.offset;
            const partialString = resolveString.substring(0, offset);
            const combinedOptions = Object.assign({}, options, { partialString: partialString });

            doRandomiserEffect(combinedOptions, () => {
                const nextOptions = Object.assign({}, options, { offset: offset + 1 });

                if (offset <= resolveString.length) {
                    doResolverEffect(nextOptions, callback);
                } else if (typeof callback === "function") {
                    callback();
                }
            });
        };

        doResolverEffect(combinedOptions, callback);
    }
};

const strings = ['MARIA KUNEVA', 'UI & UX designer']; // Add your strings here
let counter = 0;

// Get all elements with the data-target-resolver attribute
const elements = document.querySelectorAll('[data-target-resolver]');

// Start populating the elements after a delay
setTimeout(() => {
    populateElements(0); // Start populating elements from the first one
}, 1000); // 2 seconds delay before population starts

// Function to populate the elements
function populateElements(index) {
    if (index >= elements.length || counter >= strings.length) {
        return; // Stop if all elements have been populated or all strings have been used
    }

    const options = {
        // Initial position
        offset: 0,
        // Timeout between each random character
        timeout: 5,
        // Number of random characters to show
        iterations: 10,
        // Random characters to pick from
        characters: ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x', 'y', 'x', '#', '%', '&', '-', '+', '_', '?', '/', '\\', '='],
        // String to resolve
        resolveString: strings[counter],
        // The element
        element: elements[index]
    };

    // Callback function when resolve completes
    function callback() {
        if (counter === 0) {
            // Insert a delay between appearances of the strings
            setTimeout(() => {
                counter++; // Move to the next string
                populateElements(index + 1); // Populate the next element
            }, 2000); // 2 seconds delay
        } else {
            counter++; // Move to the next string
            populateElements(index + 1); // Populate the next element
        }
    }

    resolver.resolve(options, callback);
}

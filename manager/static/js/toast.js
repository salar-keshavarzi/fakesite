(function (root, factory) {
    try {
        if (typeof exports === 'object') {
            module.exports = factory();
        } else {
            root.VanillaToasts = factory();
        }
    } catch (error) {
        console.error('Isomorphic compatibility is not supported at this time for VanillaToasts.')
    }
})(this, function () {
    if (document.readyState === 'complete') {
        init();
    } else {
        window.addEventListener('DOMContentLoaded', init);
    }
    VanillaToasts = {
        create: function () {
            console.error([
                'DOM has not finished loading.',
                '\tInvoke create method when DOM\s readyState is complete'
            ].join('\n'))
        },
        setTimeout: function () {
            console.error([
                'DOM has not finished loading.',
                '\tInvoke create method when DOM\s readyState is complete'
            ].join('\n'))
        },
        toasts: {}
    };
    var autoincrement = 0;
    function init() {
        var container = document.createElement('div');
        container.id = 'vanillatoasts-container';
        document.body.appendChild(container);
        VanillaToasts.create = function (options) {
            var toast = document.createElement('div');
            toast.id = ++autoincrement;
            toast.id = 'toast-' + toast.id;
            toast.className = 'vanillatoasts-toast';
            if (options.title) {
                var h4 = document.createElement('h4');
                h4.className = 'vanillatoasts-title';
                h4.innerHTML = options.title;
                toast.appendChild(h4);
            }
            if (options.text) {
                var p = document.createElement('p');
                p.className = 'vanillatoasts-text';
                p.innerHTML = options.text;
                toast.appendChild(p);
            }
            if (options.icon) {
                var img = document.createElement('img');
                img.src = options.icon;
                img.className = 'vanillatoasts-icon';
                toast.appendChild(img);
            }
            if (options.onHide) {
                // do something
            }
            var position = options.positionClass
            switch (position) {
                case 'topLeft':
                    container.classList.add('toasts-top-left');
                    break;
                case 'bottomLeft':
                    container.classList.add('toasts-bottom-left');
                    break;
                case 'bottomRight':
                    container.classList.add('toasts-bottom-right');
                    break;
                case 'topRight':
                    container.classList.add('toasts-top-right');
                    break;
                case 'topCenter':
                    container.classList.add('toasts-top-center');
                    break;
                case 'bottomCenter':
                    container.classList.add('toasts-bottom-center');
                    break;
                default:
                    container.classList.add('toasts-top-right');
                    break;
            }
            if (typeof options.callback === 'function') {
                toast.addEventListener('click', options.callback);
            }
            toast.hide = function () {
                toast.className += ' vanillatoasts-fadeOut';
                toast.addEventListener('animationend', removeToast, false);
                if (options.onHide) {
                    options.onHide();
                }
            }
            if (options.single === true) {
                var elements = document.getElementsByClassName('vanillatoasts-toast');
                while (elements.length > 0) {
                    elements[0].parentNode.removeChild(elements[0]);
                }
            }
            if (options.timeout) {
                setTimeout(toast.hide, options.timeout);
            }

            if (options.type) {
                toast.className += ' vanillatoasts-' + options.type;
            }
            toast.addEventListener('click', toast.hide);
            function removeToast() {
                document.getElementById('vanillatoasts-container').removeChild(toast);
                delete VanillaToasts.toasts[toast.id];
            }
            document.getElementById('vanillatoasts-container').appendChild(toast);
            VanillaToasts.toasts[toast.id] = toast;

            return toast;
        }
        VanillaToasts.setTimeout = function (toastid, val) {
            if (VanillaToasts.toasts[toastid]) {
                setTimeout(VanillaToasts.toasts[toastid].hide, val);
            }
        }
    }

    return VanillaToasts;

});

const showMessage = (title, message, type) => {
    if (type === 'success') {
        VanillaToasts.create({
            title: title,
            text: message,
            type: 'success',
            icon: null,
            timeout: 4000
        });
    } else if (type === 'error') {
        VanillaToasts.create({
            title: title,
            text: message,
            type: 'error',
            icon: null,
            timeout: 4000
        });
    } else {
        VanillaToasts.create({
            title: title,
            text: message,
            type: 'info',
            icon: null,
            timeout: 4000
        });
    }
}

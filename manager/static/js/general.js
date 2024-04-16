const baseUrl = window.location.origin + '/'
window.addEventListener('scroll', (e) => {
    const header = document.getElementById("header");
    if (window.scrollY > 400) {
        header.classList.add("header-scroll");
    } else if (window.scrollY === 0) {
        header.classList.remove("header-scroll");
    }
})

document.addEventListener('click', (e) => {
    const dropdowns = document.querySelectorAll('.dropdown');
    for (const dropdown of dropdowns) {
        if (e.target !== dropdown.querySelector('input')) {
            dropdown.querySelector('.dropdown-content').style.display = 'none';
        }
    }
})

document.addEventListener('DOMContentLoaded', () => {
    const dropdown = document.querySelector('.search .dropdown');
    dropdown.querySelector('input').addEventListener('keyup', (e) => {
        if (e.target.value !== null) {
            dropdown.querySelector('.dropdown-content').style.display = 'flex';
            const UserDropdownContainer = document.querySelector('.header .user-dropdown-container.active')
            if (UserDropdownContainer) {
                UserDropdownContainer.classList.remove('active');
            }
        }
    })
    dropdown.querySelector('input').addEventListener('focus', (e) => {
        dropdown.querySelector('.dropdown-content').style.display = 'flex';
        const UserDropdownContainer = document.querySelector('.header .user-dropdown-container.active')
        if (UserDropdownContainer) {
            UserDropdownContainer.classList.remove('active');
        }
    })

    const searchInput = document.getElementById('search-input')
    searchInput.addEventListener('keyup', (e) => {
        const dropdownContent = document.querySelector('.search .dropdown-content')
        const innerItems = dropdownContent.querySelectorAll('.item')
        innerItems.forEach(item => item.remove())
        const value = e.target.value;
        if (value) {
            const dropdown = searchInput.parentNode
            const loader = dropdown.querySelector('.loader');
            loader.style.display = 'block';
            getReq(`product/list/api/?search=${value}`, 2).then((response) => {
                if (response.length > 0) {
                    response.forEach((item) => {
                        const isAvailable = dropdown.querySelector(`a[data-id='${item.id}']`)
                        if (!isAvailable) {
                            let itemElement = document.createElement('a')
                            itemElement.setAttribute('href', window.location.origin + '/product/' + item.id + '/')
                            itemElement.setAttribute('class', 'item')
                            itemElement.setAttribute('data-id', item.id)
                            let imageElement = document.createElement('img')
                            imageElement.setAttribute('src', item.image)
                            imageElement.setAttribute('alt', item.title)
                            let divElement = document.createElement('div')
                            divElement.setAttribute('class', 'title')
                            divElement.innerText = item.title
                            itemElement.appendChild(imageElement)
                            itemElement.appendChild(divElement)
                            dropdownContent.appendChild(itemElement)
                        }
                    })
                } else {
                    const temp = dropdown.querySelector('.item.not-found')
                    if (!temp) {
                        let notFoundElement = document.createElement('p')
                        notFoundElement.setAttribute('class', 'item not-found')
                        notFoundElement.style.textAlign = 'center'
                        notFoundElement.style.width = '100%'
                        notFoundElement.style.display = 'block'
                        notFoundElement.style.padding = '1rem'
                        notFoundElement.style.fontSize = '1.5rem'
                        let divElement = document.createElement('div')
                        divElement.setAttribute('class', 'title')
                        divElement.innerText = 'موردی یافت نشد'
                        divElement.style.color = '#5e5e5e'
                        notFoundElement.appendChild(divElement)
                        innerItems.forEach(item => item.remove())
                        dropdownContent.appendChild(notFoundElement)
                    }
                }
            }).catch((err) => {
                console.error(err);
            }).finally(() => {
                loader.style.display = 'none'
            });
        }
    })
})

const getReq = async (uri, type = 1) => {
    let url = uri
    if (type !== 1) {
        url = baseUrl + uri
    }
    return await fetch(url).then(response => {
        return response.json();
    }).catch(err => {
        console.error(err);
        throw err;
    })
}
const postReq = async (uri, data = null, csrf = null, type = 1) => {
    let url = uri
    if (type !== 1) {
        url = baseUrl + uri
    }
    return await fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrf
        },
    }).then(response => {
        if (response.status === 429) {
            const retryAfter = response.headers.get('Retry-After');
            console.log(retryAfter)
            return {statusCode: response.status, data: {'retryAfter': retryAfter}};
        }
        return response.json().then(data => ({statusCode: response.status, data: data}));
    }).catch(err => {
        console.error(err);
        throw err;
    })
}

document.addEventListener('DOMContentLoaded', () => {
    const sideMenuOpenBtn = document.getElementById("side-menu-btn")
    const sideMenuOverlay = document.getElementById("side-menu-overlay")
    const sideMenuCloseBtn = document.getElementById("side-menu-close-btn")
    const outOfSideMenu = document.querySelector(".out-of-side-menu")
    sideMenuOpenBtn.addEventListener('click', () => {
        sideMenuOverlay.style.display = 'flex'
    })
    sideMenuCloseBtn.addEventListener('click', () => {
        sideMenuOverlay.style.display = 'none'
    })
    outOfSideMenu.addEventListener('click', () => {
        sideMenuOverlay.style.display = 'none'
    })
    // document.addEventListener("click", (e) => {
    //     if (e.target !== sideMenu && e.target !== sideMenuOpenBtn) {
    //         sideMenu.style.display = 'none'
    //     }
    // })
})

document.addEventListener('DOMContentLoaded', () => {
    const priceElements = document.querySelectorAll('.price-element')
    priceElements.forEach(ele => {
        const newtext = new Intl.NumberFormat().format(ele.textContent)
        ele.innerHTML = newtext
    })
})


// document.addEventListener('DOMContentLoaded', () => {
//     const userNavigationContainer = document.querySelector('.user-navigate-section')
//     const activeNavigationBtn = document.querySelector('.active-navigation-btn')
//     activeNavigationBtn.onclick = () => {
//         userNavigationContainer.classList.toggle('active')
//         if (userNavigationContainer.classList.contains('active')) {
//             activeNavigationBtn.innerHTML = 'بستن منوی کاربری'
//         } else {
//             activeNavigationBtn.innerHTML = 'نمایش منوی کاربری'
//         }
//     }
// })


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

// (function (root, factory) {
//     try {
//         if (typeof exports === 'object') {
//             module.exports = factory();
//         } else {
//             root.VanillaToasts = factory();
//         }
//     } catch (error) {
//         console.log('Isomorphic compatibility is not supported at this time for VanillaToasts.')
//     }
// })(this, function () {
//     if (document.readyState === 'complete') {
//         init();
//     } else {
//         window.addEventListener('DOMContentLoaded', init);
//     }
//     VanillaToasts = {
//         create: function () {
//             console.error([
//                 'DOM has not finished loading.',
//                 '\tInvoke create method when DOM\s readyState is complete'
//             ].join('\n'))
//         },
//         setTimeout: function () {
//             console.error([
//                 'DOM has not finished loading.',
//                 '\tInvoke create method when DOM\s readyState is complete'
//             ].join('\n'))
//         },
//         toasts: {}
//     };
//     var autoincrement = 0;
//     function init() {
//         var container = document.createElement('div');
//         container.id = 'vanillatoasts-container';
//         document.body.appendChild(container);
//         VanillaToasts.create = function (options) {
//             var toast = document.createElement('div');
//             toast.id = ++autoincrement;
//             toast.id = 'toast-' + toast.id;
//             toast.className = 'vanillatoasts-toast';
//             if (options.title) {
//                 var h4 = document.createElement('h4');
//                 h4.className = 'vanillatoasts-title';
//                 h4.innerHTML = options.title;
//                 toast.appendChild(h4);
//             }
//             if (options.text) {
//                 var p = document.createElement('p');
//                 p.className = 'vanillatoasts-text';
//                 p.innerHTML = options.text;
//                 toast.appendChild(p);
//             }
//             if (options.icon) {
//                 var img = document.createElement('img');
//                 img.src = options.icon;
//                 img.className = 'vanillatoasts-icon';
//                 toast.appendChild(img);
//             }
//             if (options.onHide) {
//                 // do something
//             }
//             var position = options.positionClass
//             switch (position) {
//                 case 'topLeft':
//                     container.classList.add('toasts-top-left');
//                     break;
//                 case 'bottomLeft':
//                     container.classList.add('toasts-bottom-left');
//                     break;
//                 case 'bottomRight':
//                     container.classList.add('toasts-bottom-right');
//                     break;
//                 case 'topRight':
//                     container.classList.add('toasts-top-right');
//                     break;
//                 case 'topCenter':
//                     container.classList.add('toasts-top-center');
//                     break;
//                 case 'bottomCenter':
//                     container.classList.add('toasts-bottom-center');
//                     break;
//                 default:
//                     container.classList.add('toasts-top-right');
//                     break;
//             }
//             if (typeof options.callback === 'function') {
//                 toast.addEventListener('click', options.callback);
//             }
//             toast.hide = function () {
//                 toast.className += ' vanillatoasts-fadeOut';
//                 toast.addEventListener('animationend', removeToast, false);
//
//                 if (options.onHide) {
//                     options.onHide();
//                 }
//             }
//             if (options.single === true) {
//                 var elements = document.getElementsByClassName('vanillatoasts-toast');
//                 while (elements.length > 0) {
//                     elements[0].parentNode.removeChild(elements[0]);
//                 }
//             }
//             if (options.timeout) {
//                 setTimeout(toast.hide, options.timeout);
//             }
//             if (options.type) {
//                 toast.className += ' vanillatoasts-' + options.type;
//             }
//             toast.addEventListener('click', toast.hide);
//             function removeToast() {
//                 document.getElementById('vanillatoasts-container').removeChild(toast);
//                 delete VanillaToasts.toasts[toast.id];  //remove toast from object
//             }
//             document.getElementById('vanillatoasts-container').appendChild(toast);
//             VanillaToasts.toasts[toast.id] = toast;
//             return toast;
//         }
//         VanillaToasts.setTimeout = function (toastid, val) {
//             if (VanillaToasts.toasts[toastid]) {
//                 setTimeout(VanillaToasts.toasts[toastid].hide, val);
//             }
//         }
//     }
//
//     return VanillaToasts;
//
// });
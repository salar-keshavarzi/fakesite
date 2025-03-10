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
})

document.addEventListener('DOMContentLoaded', () => {
    const priceElements = document.querySelectorAll('.price-element')
    priceElements.forEach(ele => {
        ele.innerHTML = new Intl.NumberFormat().format(ele.innerText)
    })
})




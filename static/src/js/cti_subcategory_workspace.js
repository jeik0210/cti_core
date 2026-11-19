/** @odoo-module **/

document.addEventListener('click', (event) => {
    const groupToggle = event.target.closest('[data-cti-group-toggle]');
    if (groupToggle) {
        const menu = document.getElementById(groupToggle.dataset.ctiGroupToggle);
        if (menu) {
            const expanded = groupToggle.getAttribute('aria-expanded') === 'true';
            groupToggle.setAttribute('aria-expanded', String(!expanded));
            menu.hidden = expanded;
            const indicator = groupToggle.querySelector('.o_cti_workspace_group_indicator');
            if (indicator) {
                indicator.classList.toggle('fa-plus-square-o', expanded);
                indicator.classList.toggle('fa-minus-square-o', !expanded);
            }
        }
        return;
    }
    const button = event.target.closest('[data-cti-panel]');
    if (!button) {
        return;
    }

    const workspace = button.closest('.o_cti_subcategory_workspace');
    if (!workspace) {
        return;
    }

    const selectedPanel = button.dataset.ctiPanel;
    workspace.querySelectorAll('[data-cti-panel]').forEach((item) => {
        const selected = item === button;
        item.classList.toggle('active', selected);
        item.setAttribute('aria-expanded', String(selected));
    });
    workspace.querySelectorAll('[data-cti-content]').forEach((panel) => {
        panel.hidden = panel.dataset.ctiContent !== selectedPanel;
    });
});

document.addEventListener('submit', (event) => {
    if (!event.target.matches('.o_cti_phone_form')) {
        return;
    }
    event.preventDefault();
    const form = event.target;
    let message = form.querySelector('.o_cti_form_notice');
    if (!message) {
        message = document.createElement('p');
        message.className = 'o_cti_form_notice';
        message.setAttribute('role', 'status');
        form.appendChild(message);
    }
    message.textContent = 'El formulario está listo. La consulta aún no está conectada.';
});

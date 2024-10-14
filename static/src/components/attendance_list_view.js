/** @odoo-module */

import { registry } from "@web/core/registry"
import { listView } from "@web/views/list/list_view"
import { ListController } from "@web/views/list/list_controller"
const { onMounted } = owl


class AttendanceListViewController extends ListController {
    setup() {
        console.log("Attendance list inherited!")
        super.setup()

        onMounted(() => {
            this.controlPanel()
            this.setupFilterButtonListener()
            this.loadSavedDates()
            this.setupClearFilterListener()
            this.setupDateFieldListeners()
            this.loadData('hr.branch', 'sucursal', 'Suc.')
            this.loadData('hr.department', 'departamento', 'Depto.')
            this.loadData('hr.employee', 'empleado', 'Emp.')
        })
    }

    controlPanel() {
        const controlPanel = document.querySelector(".o_control_panel")
        if (controlPanel) {
            const newDiv = document.createElement('div')
            newDiv.className = 'o_onboarding_panel'
            newDiv.style.cssText = 'display: flex; align-items: center; justify-content: space-between; width: 96%; margin: 0.5% 2%;'
            newDiv.innerHTML = `
            <div class="o_onboarding_panel_step d-flex align-items-center">
                <form class="d-flex align-items-center">
                
                <!-- Filtro por sucursal -->
                <label for="sucursal" class="me-2">Sucursal:</label>
                    <select id="sucursal" name="sucursal" class="form-select me-4 border rounded p-2">
                    <option value="">Seleccione Suc.</option>
                    <option value="sucursal1">Sucursal 1</option>
                        <option value="sucursal2">Sucursal 2</option>
                        <option value="sucursal3">Sucursal 3</option>
                    </select>

                    <!-- Filtro por departamento -->
                    <label for="departamento" class="me-2">Departamento:</label>
                    <select id="departamento" name="departamento" class="form-select me-4 border rounded p-2">
                        <option value="">Seleccione Depto.</option>
                        <option value="departamento1">Departamento 1</option>
                        <option value="departamento2">Departamento 2</option>
                        <option value="departamento3">Departamento 3</option>
                    </select>

                    <!-- Filtro por empleado -->
                    <label for="empleado" class="me-2">Empleado:</label>
                    <select id="empleado" name="empleado" class="form-select me-4 border rounded p-2">
                    <option value="">Seleccione Emp.</option>
                    <option value="empleado1">Empleado 1</option>
                        <option value="empleado2">Empleado 2</option>
                        <option value="empleado3">Empleado 3</option>
                    </select>
                        
                    <!-- Fecha desde -->
                    <label for="date_from" class="me-2">Desde:</label>
                    <input type="text" placeholder="Ingrese la fecha" id="date_from" name="date_from" class="form-control me-4 border rounded p-2" />
    
                    <!-- Fecha hasta -->
                    <label for="date_to" class="me-2">Hasta:</label>
                    <input type="text" placeholder="Ingrese la fecha" id="date_to" name="date_to" class="form-control me-4 border rounded p-2" />
                    
                    <!-- Botón Aplicar -->
                    <button type="submit" class="btn btn-primary">
                        Aplicar
                    </button>

                    <!-- Botón Borrar Filtro -->
                    <a class="btn btn-outline-dark ms-3 text-nowrap">
                        BORRAR FILTRO
                    </a>
                </form>
            </div>
            `
            controlPanel.appendChild(newDiv)
        }
    }

    setupFilterButtonListener() {
        const filterButton = document.querySelector('.o_onboarding_panel form button[type="submit"]')
        if (filterButton) {
            filterButton.addEventListener('click', (event) => {
                event.preventDefault()
                const dateFrom = document.getElementById('date_from')
                const dateTo = document.getElementById('date_to')
                
                if (dateFrom && dateTo) {
                    this.saveDates(dateFrom.value, dateTo.value)
                    this.applyDateFilter(dateFrom.value, dateTo.value)
                } else {
                    console.warn('No se encontraron los campos de fecha')
                }
            })
        } else {
            console.warn('No se encontró el botón de filtrar')
        }
    }

    saveDates(dateFrom, dateTo) {
        localStorage.setItem('attendanceDateFrom', dateFrom)
        localStorage.setItem('attendanceDateTo', dateTo)
    }

    loadSavedDates() {
        const dateFrom = localStorage.getItem('attendanceDateFrom')
        const dateTo = localStorage.getItem('attendanceDateTo')
        
        if (dateFrom) {
            document.getElementById('date_from').value = dateFrom
        }
        if (dateTo) {
            document.getElementById('date_to').value = dateTo
        }
    }

    setupClearFilterListener() {
        const clearFilterButton = document.querySelector('.o_onboarding_panel a.btn-outline-dark')
        if (clearFilterButton) {
            clearFilterButton.addEventListener('click', (event) => {
                event.preventDefault()
                this.clearFilters()
            })
        } else {
            console.warn('No se encontró el botón de borrar filtro')
        }
    }

    clearFilters() {
        // Limpiar fechas en localStorage
        localStorage.removeItem('attendanceDateFrom')
        localStorage.removeItem('attendanceDateTo')

        // Limpiar todos los campos de filtro
        document.getElementById('date_from').value = ''
        document.getElementById('date_to').value = ''
        document.getElementById('sucursal').value = ''
        document.getElementById('departamento').value = ''
        document.getElementById('empleado').value = ''

        // Volver a la vista original
        this.env.services.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Asistencias',
            res_model: 'hr.attendance',
            view_mode: 'list',
            views: [[false, 'list']],
            target: 'current',
            domain: [],
        })
    }

    applyDateFilter(dateFrom, dateTo) {
        const sucursalSelect = document.getElementById('sucursal');
        const departamentoSelect = document.getElementById('departamento');
        const empleadoSelect = document.getElementById('empleado');

        const sucursalSeleccionada = sucursalSelect && sucursalSelect.value;
        const departamentoSeleccionado = departamentoSelect && departamentoSelect.value;
        const empleadoSeleccionado = empleadoSelect && empleadoSelect.value;

        if (!dateFrom && !dateTo && !sucursalSeleccionada && !departamentoSeleccionado && !empleadoSeleccionado) {
            console.warn('No se ha seleccionado ningún filtro. No se aplicará ningún cambio.');
            return;
        }

        const formatDate = (dateString) => {
            if (!dateString) return '';
            const date = new Date(dateString);
            return date.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' });
        };

        const formattedDateFrom = formatDate(dateFrom);
        const formattedDateTo = formatDate(dateTo);

        let name = '';
        if (formattedDateFrom && formattedDateTo) {
            name += ` (${formattedDateFrom} - ${formattedDateTo})`;
        } else if (formattedDateFrom) {
            name += ` (Desde: ${formattedDateFrom})`;
        } else if (formattedDateTo) {
            name += ` (Hasta: ${formattedDateTo})`;
        }

        const domain = [];
        if (dateFrom) {
            domain.push(['date_in', '>=', dateFrom]);
        }
        if (dateTo) {
            domain.push(['date_in', '<=', dateTo]);
        }

        // Añadir filtro por sucursal
        if (sucursalSeleccionada) {
            domain.push(['employee_id.branch_id', '=', parseInt(sucursalSeleccionada)]);
            name += ` (Suc. ${sucursalSelect.options[sucursalSelect.selectedIndex].text})`;
        }

        // Añadir filtro por departamento
        if (departamentoSeleccionado) {
            domain.push(['employee_id.department_id', '=', parseInt(departamentoSeleccionado)]);
            name += ` (Depto. ${departamentoSelect.options[departamentoSelect.selectedIndex].text})`;
        }

        // Añadir filtro por empleado
        if (empleadoSeleccionado) {
            domain.push(['employee_id', '=', parseInt(empleadoSeleccionado)]);
            name += ` (Emp. ${empleadoSelect.options[empleadoSelect.selectedIndex].text})`;
        }

        this.env.services.action.doAction({
            type: 'ir.actions.act_window',
            name: name,
            res_model: 'hr.attendance',
            view_mode: 'list',
            views: [[false, 'list']],
            target: 'current',
            domain: domain,
        });
    }

    setupDateFieldListeners() {
        const dateFields = ['date_from', 'date_to']
        dateFields.forEach(fieldId => {
            const field = document.getElementById(fieldId)
            if (field) {
                field.addEventListener('click', function() {
                    this.type = 'date'
                    if (this.showPicker) {
                        this.showPicker()
                    }
                })
                field.addEventListener('blur', function() {
                    if (this.value === '') {
                        this.type = 'text'
                    }
                })
            } else {
                console.warn(`No se encontró el campo ${fieldId}`)
            }
        })
    }

    async loadData(model, selectId, labelText) {
        try {
            const result = await this.orm.call(
                model,
                'search_read',
                [[]],
                {
                    fields: ['id', 'name'],
                    limit: 0,
                }
            );
            this.updateSelect(selectId, result, labelText);
        } catch (error) {
            console.error(`Error al cargar ${selectId}:`, error);
        }
    }

    updateSelect(selectId, options, labelText) {
        const select = document.getElementById(selectId);
        if (select) {
            select.innerHTML = `<option value="">Seleccione ${labelText}</option>`;
            options.forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option.id;
                optionElement.textContent = option.name;
                select.appendChild(optionElement);
            });
        } else {
            console.warn(`No se encontró el select de ${selectId}`);
        }
    }
}

const attendanceListView = {
    ...listView,
    Controller: AttendanceListViewController,
}

registry.category("views").add("attendance_list_view", attendanceListView)

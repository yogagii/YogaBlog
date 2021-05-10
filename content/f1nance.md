Title: Digitalizing Intelligence in Finance Reporting
Date: 2021-05-10
Category: Project
Tags: Tableau, SAP
Author: Yoga

## Background

The Digital Platform is a web application that hosts finance reports, training, access management, and incident management. When accessing reports, the Digital Platform provides users a personalized experience. The increasing number of users interacting with reports online creates a huge data set that gives us millions of potential insights into user experience, personalization, and finance report improvements. AI technologies such as Market basket analysis and collaboration filtering methods are deployed to learn users’ behaviors and recommend the relevant finance reports in real-time. Based on the user’s persona, different personalized announcements, training, and finance reports are prioritized.

The Digital Platform is an innovative solution for finance reports including a creative way to source the data, customizable machine learning algorithm to improve user experience. To source the data from different technologies servers, Google Analytics is deployed to track every users’ behavior. Machine learning Recommendation Engine is implemented to study the user’s behavior. Users are split into Cold and Hot User based on the view history.

link: https://yogagii.github.io/recommend-system.html

## Business Value

There are more than 600 finance users actively utilize the platform service every month. Because of the good customizable personal user experience, the utilization of the platform is to keep increasing. Every user uses 8.2 times of the Digital Platform every month. User's experiences are improved and users spend more than 700 hours per month on the Digital Platform. The digital platform is providing users the customized personalized experience also keeping improve the financial reporting based on feedback.


# Dashboard

![f1nance](img/f1nance1.png)
![f1nance](img/f1nance3.png)

# Tableau Report

![f1nance](img/f1nance2.png)

## Tableau REST API:

Description | API | Params
- | - | -
Get Users in Group | GET /api/api-version/sites/site-id/groups/group-id/users | pageSize
Get Users on Site	| GET /api/api-version/sites/site-id/users | pageSize, filter
Query Views for Site | GET /api/api-version/sites/site-id/views | includeUsageStatistics, fields, pageNumber
Query Views for Workbook | GET /api/api-version/sites/site-id/workbooks/workbook-id/views | 
Query Workbook | GET /api/api-version/sites/site-id/workbooks/workbook-id | 
Query Workbook Permissions | GET /api/api-version/sites/site-id/workbooks/workbook-id/permissions | 
Query Workbooks for User | GET /api/api-version/sites/site-id/users/user-id/workbooks | pageSize, pageNumber

link: https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref.htm

## Viz Option:

Key | Value
- | -
hideTabs | true
':toolbar' | 'top'
':showShareOptions' | false
':render' | false
width | '100%'

## Viz API:

Class | Properties | Type | Description
- | - | - | -
Viz | getWorkbook() | Workbook | One Workbook is supported per visualization.
Workbook | getActiveSheet() | Sheet | Gets the currently active sheet (the active tab)
SheetInfo | getName() | string | Gets the name of the sheet.
SheetInfo | getUrl() | string	| Gets the URL for this sheet.
SheetInfo | getSheetType() | SheetType | Gets the type of the sheet. SheetType is an enum with the following values: WORKSHEET, DASHBOARD and STORY.
Dashboard | getWorksheets() | Worksheet[] | Gets the collection of worksheets contained in the dashboard.
Worksheet | getFiltersAsync() | Promise<Filter[]> | Fetches the collection of filters used on the sheet.
Workbook | getParametersAsync() | Promise<Parameter[]> | Fetches the parameters for this workbook.
Workbook | getCustomViewsAsync() | Promise<CustomView[]> | Gets the collection of CustomView objects associated with the workbook.
Filter | getFieldName() | string | Gets the name of the field being filtered.
CategoricalFilter | getAppliedValues() | DataValue[] | Gets the collection of values that are currently set on the filter.
Parameter | getCurrentValue() | DataValue | The current value of the parameter.

## Viz Event Classes:

Name | Event Class Passed in the Callback | Description
- | - | -
CUSTOM_VIEW_LOAD | CustomViewEvent | Raised when a custom view has finished loading.
PARAMETER_VALUE_CHANGE | ParameterEvent | Raised when any parameter has changed state.
FILTER_CHANGE | FilterEvent | Raised when any filter has changed state.
TAB_SWITCH | TabSwitchEvent | Raised after the tab switched.

link: https://help.tableau.com/v2018.2/api/js_api/en-us/JavaScriptAPI/js_api_ref.htm

```js
const Workbook = ({ workbook, userDetail, siteConfig, edit, changedFilter }) => {
  const [url, setUrl] = useState('');

  option[id] = {
    hideTabs: true,
    ':toolbar': 'top',
    ':showShareOptions': false,
    ':linktarget': '_self',
    ':render': false,
    width: '100%',
    onFirstInteractive: () => {
      mainWorkbook = viz[id].getWorkbook();
      const _tabName = mainWorkbook.getActiveSheet().getName();
      const _tabKey = current.tabs?.find(tab => tab.name === _tabName);
      if (_tabKey && _tabKey.contentUrl) {
        setTabName(_tabKey.contentUrl.split('/').pop());
      } else {
        setTabName(_tabName);
      }
      if (isMix) {
        // Fetch all the filter
        if (mainWorkbook.getActiveSheet().getSheetType() === 'worksheet') {
          worksheets.push(mainWorkbook.getActiveSheet());
        } else {
          worksheets = mainWorkbook.getActiveSheet().getWorksheets();
        }
        const arr = [];
        worksheets.forEach(sheet => {
          arr.push(
            sheet.getFiltersAsync().then(filters => {
              return filters.map(filter => ({
                name: filter.getFieldName(),
                type: 'filter',
              }));
            }),
          );
        });
        // Fetch all the parameters
        arr.push(
          mainWorkbook.getParametersAsync().then(parameters => {
            return parameters.map(param => ({
              name: param.getName(),
              type: 'param',
            }));
          }),
        );
        Promise.all(arr).then(filters => {
          const filterNames = new Set();
          const reportFilters = [];
          filters.forEach(data => {
            data.forEach(filter => {
              if (!filterNames.has(filter.name)) {
                filterNames.add(filter.name);
                reportFilters.push(filter);
              }
            });
          });
        });
      }
      // Fetch all the collection
      mainWorkbook.getCustomViewsAsync().then(customViews => {
        const impl = '_impl';
        viewlists.viewlistMy = [];
        viewlists.viewlistOther = [];

        customViews.forEach(view => {
          if (
            view[impl].$i.owner.username.toLowerCase().indexOf(userDetail.userId.toLowerCase()) > -1
          ) {
            viewlists.viewlistMy.push({
              id: view[impl].$i.id,
              name: view[impl].$i.name,
              url: view[impl].$i.url,
            });
          } else {
            viewlists.viewlistOther.push({
              id: view[impl].$i.id,
              name: view[impl].$i.name,
              url: view[impl].$i.url,
            });
          }
        });
        viewlists.viewlistMy.sort((a, b) => b.id - a.id);
        setViewlist({
          ...viewlist,
          loading: false,
          viewlistMy: viewlists.viewlistMy,
          viewlistOther: viewlists.viewlistOther,
        });
      });
      viz[id].addEventListener('customviewload', () => {
        setViewlist({
          ...viewlist,
          ...viewlists,
          loading: false,
        });
      });
      viz[id].addEventListener(window.tableau.TableauEventName.TAB_SWITCH, tabsEvent => {
        const _tabUrl = tabsEvent
          .getViz()
          .getWorkbook()
          .getActiveSheet()
          .getUrl();
        const _tabName = _tabUrl.split('/').pop();
        setTabName(_tabName);
        window.history.pushState(null, null, `${window.location.pathname}?tab=${_tabName}`);
      });
      if (isMix) {
        viz[id].addEventListener(window.tableau.TableauEventName.FILTER_CHANGE, filterEvent => {
          filterEvent.getFilterAsync().then(filter => {
            dispatch({
              type: 'webiWorkbook/changeFilter',
              payload: {
                data: {
                  name: filter.getFieldName(),
                  value: filter.getAppliedValues().map(i => i.value),
                },
                id,
              },
            });
          });
        });
        viz[id].addEventListener(
          window.tableau.TableauEventName.PARAMETER_VALUE_CHANGE,
          parameterEvent => {
            parameterEvent.getParameterAsync().then(parameter => {
              dispatch({
                type: 'webiWorkbook/changeFilter',
                payload: {
                  data: {
                    name: parameter.getName(),
                    value: parameter.getCurrentValue().formattedValue,
                  },
                  id,
                },
              });
            });
          },
        );
      }
    },
  };

  // add tableau session in IE11
  useEffect(() => {
    if (
      !document.getElementById('myFrame') &&
      !!window.MSInputMethodContext &&
      !!document.documentMode
    ) {
      const ifrm = document.createElement('iframe');
      ifrm.setAttribute('id', 'myFrame');
      ifrm.setAttribute('src', siteConfig.tableBaseUrl);
      ifrm.style.width = '0';
      ifrm.style.height = '0';
      document.body.appendChild(ifrm);
      const ifr = document.getElementById('myFrame');
      ifr.onload = () => {
        if (!document.cookie.match(/^(.*;)?\s*frameLoaded\s*=\s*[^;]+(.*)?$/)) {
          const delay = (() => {
            let timer = 0;
            return (callback, ms) => {
              clearTimeout(timer);
              timer = setTimeout(callback, ms);
            };
          })();
          delay(() => {
            document.cookie = 'frameLoaded=yes; expires=Sun, 1 Jan 2023 00:00:00 UTC; path=/';
            window.location.reload();
          }, 5000);
        }
      };
    }
  }, [siteConfig.tableBaseUrl]);

  // Combine the workbook url with the location search
  useEffect(() => {
    let urlTemp = null;
    if (current.id !== id) {
      return () => {};
    }
    urlTemp = current.content_url || current.document_url;
    if (isEdit) {
      const { content } = current;
      urlTemp = `${siteConfig.tableBaseUrl}/t/WWFPA/authoring/`;
      urlTemp = `${urlTemp +
        content.slice(0, content.indexOf('/')) +
        content.slice(content.lastIndexOf('/'))}#1`;
    } else if (location.search) {
      const searchParams = new URLSearchParams(location.search);
      if (location.search.indexOf('share') > -1) {
        const share = searchParams.get('share');
        urlTemp = `${urlTemp}?share=${share}`;
      }
      if (location.search.indexOf('?tab') > -1) {
        let tab = searchParams.get('tab');
        setTabName(tab);
        urlTemp = `${urlTemp}/${tab}`;
      }
    }
    setUrl(urlTemp);
  }, [isEdit, current, id, location.search, siteConfig.tableBaseUrl]);

  // When set url, it will render workbook by Viz, the follow code is the detail.
  useEffect(() => {
    if (current.id === id && url) {
      try {
        viz[id] && viz[id].dispose();
        console.time('tableau');
        tableauStart = new Date().getTime();
        const vizContainer = document.getElementById(`vizContainer${id}`);
        if (vizContainer) {
          if (window.tableau) {
            console.log('>>> new viz', url);
            viz[id] = new window.tableau.Viz(iframeContent[id], url, option[id]);
            vizContainer
              .getElementsByTagName('iframe')[0]
              .setAttribute(
                'sandbox',
                'allow-scripts allow-forms allow-same-origin allow-popups allow-top-navigation allow-downloads',
              );
          } else {
            const div = document.createElement('div');
            div.setAttribute('style', messageStyle);
            div.innerHTML = errorMessage.tableau;
            vizContainer.appendChild(div);
          }
        }
      } catch (e) {
        console.error(e);
      }
    }
  }, [current.id, current.no_tabs, id, url, userDetail.userId, location.pathname]);

  return (
    <div className={styles.vizContainerWrapper}>
      <div
        id={`vizContainer${id}`}
        ref={node => {
          iframeContent[id] = node;
        }}
        className={styles.vizContainer}
      />
    </div>
  );
};

export default Workbook;
```

### split report

![f1nance](img/f1nance4.png)
![f1nance](img/f1nance5.png)

### interactive training

![f1nance](img/f1nance6.png)

### share customized view

![f1nance](img/f1nance7.png)

# SAP Report

![f1nance](img/f1nance8.png)

## FIlter for report:

Description | Store | Function | Action | Parameter
- | - | - | - | -
get report filter list | getReportStore | getInputControls | / | viewContext
get report filter detail | getReportInputControlStore | getInputControl | / | viewContext, inputControlId
get report filter options | getReportInputControlStore | getLov | / | viewContext, inputControlId
get report filter value | getReportInputControlStore | getSelection | / | viewContext, inputControlId
set report filter value | / | / | USER_SET_INPUT_CONTROL_SELECTION | viewContext, inputControlId, selection

## FIlter for document:

Description | Store | Function | Action | Parameter
- | - | - | - | -
get document filter list | getDocumentStore | getInputControls | / | viewContext
get document filter detail | getDocumentInputControlStore | getInputControl | / | viewContext, inputControlId
get document filter options | getDocumentInputControlStore | getLov | / | viewContext, inputControlId
get document filter value | getDocumentInputControlStore | getSelection | / | viewContext, inputControlId
set document filter value | / | / | USER_SET_INPUT_CONTROL_SELECTION | viewContext, inputControlId, selection

## SAP Prompt Function:

Description | Store | Function | Action | Parameter
- | - | - | - | -
activate prompt options | / | / | GET_PARAMETER_LOV | viewContext, parameterId, (prepare, data)
get prompt value | getDocumentStore | getParameters | / | viewContext
get prompt options | getParameterStore | getLov | / | viewContext, parameterId
set prompt value | / | / | USER_VALIDATE_PROMPTS | viewContext, inputControlId, selection

## SAP Driller Function:

Description | Store | Function | Action | Parameter
- | - | - | - | -
get driller current list | getReportStore | getDrillerElements | / | viewContext
get driller all list | getReportStore | getDrillerFilters | / | viewContext
get driller detail | getDrillerFilterStore | getDrillerFilter | / | viewContext, filterId

## Post Message:

Description | Type | Value | Interval
- | - | - | -
Code injection finished | string | 'SAP_WEBI_INJECTED' | false
Filter data | object | { type: 'filters-selection', data: filters, docId: getWebiViewerArgs().id } | true
Tab data | object | { type: 'tab-selection', data: tab, docId: getWebiViewerArgs().id } | true
Prompt data | object | { type: 'parameter-selection', data: parameters, docId: getWebiViewerArgs().id } | true
Click link event | object | { type: 'document-url', data: item.href, docId: getWebiViewerArgs().id } | false

## Code Injection:

![f1nance](img/f1nance9.png)

# Design of other page

![f1nance](img/f1nance14.png)
![f1nance](img/f1nance10.png)
![f1nance](img/f1nance11.png)
![f1nance](img/f1nance12.png)
![f1nance](img/f1nance13.png)
![f1nance](img/f1nance15.png)
![f1nance](img/f1nance16.png)
![f1nance](img/f1nance17.png)
![f1nance](img/f1nance18.png)
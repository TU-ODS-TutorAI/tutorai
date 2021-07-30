## Machine Learning QnA Engine API

### API URL
 ```
/tutorai/machine_learning/<question>/<context> (GET)
```

### Argument

| Name     | Type   | Required | Constraint | Description |
| -------- | ------ | -------- | ---------- | ----------- |
| question | String | yes      |            |             |
| context  | String | yes      |            | String that contains information to answere the question            |

### Return

| Name  | Type   | Description         |
| ----- | ------ | ------------------- |
| answere | String |                   |


### API URL
 ```
/tutorai/machine_learning_with_module/<question>/<module_number> (GET)
```

### Argument

| Name     | Type   | Required | Constraint | Description |
| -------- | ------ | -------- | ---------- | ----------- |
| question | String | yes      |            |             |
| module_number  | int | yes      |            | Module Id Number            |

### Return

| Name  | Type   | Description         |
| ----- | ------ | ------------------- |
| answere | String |                   |

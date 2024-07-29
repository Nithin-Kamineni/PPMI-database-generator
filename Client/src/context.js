/* eslint-disable */
import PropTypes from 'prop-types';
import { createContext, useState, useEffect } from 'react';
import axios from 'axios';

// initial state
const initialState = {
    test: 1
};

// ==============================|| CONFIG CONTEXT & PROVIDER ||============================== //

const ParametersContext = createContext(initialState);

const url = 'http://localhost:8021/v1/';

function ParamProvider({ children }) {
    const [open, setOpen] = useState(false);

    const [varibleNames, setVaribleNames] = useState([]);
    const [fileNames, setFileNames] = useState({});

    const [selectedVariables, setSelectedVariables] = useState([]);
    const handleAutocompleteChange = (event, newValue) => {
        // setSelectedVariables(new Set(newValue));
        setSelectedVariables(Array.from(new Set(newValue)));
    };

    const [globalVaribles, setGlobalVaribles] = useState([]);
    const handleGlobalVaribles = () => {
        // setSelectedVariables(new Set(newValue));
        setGlobalVaribles(Array.from(new Set([...selectedVariables, ...globalVaribles])));
    };

    const DeleteGlobalVaribles = (globalVarible) => {
        setGlobalVaribles(globalVaribles.filter((globalVaribleTemp) => globalVarible !== globalVaribleTemp));
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(url + 'varibles');
                setVaribleNames(response.data.varibles);
                setFileNames(response.data.files);

                // console.log('varibleNames', varibleNames);
                // console.log('fileNames', Object.keys(response.data.files));
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, []);

    const [taskId, setTaskId] = useState('');
    const [showError, setShowError] = useState(false);
    const [MessageNColor, setMessageNColor] = useState(null);
    const handleSnakBar = (color, message) => {
        setShowError(true);
        setMessageNColor({ color: color, message: message });
    };

    const generateGlobalVaribles = async () => {
        if (globalVaribles.length == 0) {
            handleSnakBar('error', 'Need more than 2 column varibles in Varible list to generate data file!');
        } else {
            try {
                const response = await axios.post(url + 'generate', globalVaribles);
                console.log('response', response.data.task_id);
                setTaskId(response.data.task_id);
                handleSnakBar('success', `Request processing to generate files\ntask ID: ${response.data.task_id}`);
                setOpen(true);
            } catch (error) {
                console.error('Error fetching data:', error);
                handleSnakBar('error', `Error in request processing ${error}`);
            }
        }
    };

    return (
        <ParametersContext.Provider
            value={{
                varibleNames,
                setVaribleNames,
                fileNames,
                setFileNames,
                selectedVariables,
                handleAutocompleteChange,
                globalVaribles,
                handleGlobalVaribles,
                DeleteGlobalVaribles,
                showError,
                MessageNColor,
                setShowError,
                generateGlobalVaribles,
                open,
                setOpen,
                taskId
            }}
        >
            {children}
        </ParametersContext.Provider>
    );
}

export { ParamProvider, ParametersContext };

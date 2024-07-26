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

function ParamProvider({ children }) {

    const [varibleNames, setVaribleNames] = useState(new Set())

    return (
        <ParametersContext.Provider
            value={{
                varibleNames,
                setVaribleNames
            }}
        >
            {children}
        </ParametersContext.Provider>
    );
}

export { ParamProvider, ParametersContext };

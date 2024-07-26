import React, { useState, useEffect } from 'react';
import MainCard from 'ui-component/cards/MainCard';
import GraphComponent2 from 'ui-component/GraphComponent2';
import LinearProgress from '@mui/material/LinearProgress';
import axios from 'axios';
import { ChakraProvider, NumberInput,
    NumberInputField,
    NumberInputStepper,
    NumberIncrementStepper,
    NumberDecrementStepper,
    Select } from '@chakra-ui/react';
import { Typography, Button, Box, FormControl, InputLabel, MenuItem, Slider } from '@mui/material';
import { ParametersContext } from '../../../context';

const marks = [
    {
        value: 0.015,
        label: '0.015'
    },
    {
        value: 0.035,
        label: '0.035'
    }
];

function valuetext(value) {
    return `${value}°C`;
}

// const url = "http://nano-tumor.phhp.ufl.edu/api/model";

const SearchByFile = () => {
    // const useConfig = () => useContext(ConfigContext);
    const useParams = () => React.useContext(ParametersContext);

    let { varibleNames, setVaribleNames } = useParams();

    return (
        <ChakraProvider>
            <MainCard title="Search by files">
                edit here2
            </MainCard>
        </ChakraProvider>
    );
};

export default SearchByFile;

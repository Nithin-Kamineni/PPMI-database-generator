/* eslint-disable */

import React, { useState, useContext } from 'react';
import MainCard from 'ui-component/cards/MainCard';
import { Button, Box, TextField, Stack, Chip, LinearProgress, Divider } from '@mui/material';
import Autocomplete from '@mui/material/Autocomplete';
import { ParametersContext } from '../../../context';
import VariableList from './Variable_list';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';

import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import CloudDownloadIcon from '@mui/icons-material/CloudDownload';

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4
};

const SearchByVaribles = () => {
    const useParams = () => useContext(ParametersContext);
    let {
        varibleNames,
        selectedVariables,
        handleAutocompleteChange,
        handleGlobalVaribles,
        showError,
        setShowError,
        MessageNColor,
        open,
        setOpen,
        taskId
    } = useParams();

    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }

        setShowError(false);
    };
    return (
        <>
            <Snackbar
                open={showError}
                autoHideDuration={2000}
                onClose={handleClose}
                anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
            >
                <Alert
                    onClose={handleClose}
                    severity={MessageNColor ? MessageNColor.color : 'error'}
                    variant="filled"
                    sx={{ width: '100%' }}
                >
                    {MessageNColor ? MessageNColor.message : 'I love snacks'}
                </Alert>
            </Snackbar>
            <Modal
                open={open}
                onClose={() => setOpen(false)}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box sx={style}>
                    <Typography id="modal-modal-title" variant="h6" component="h2">
                        Task Status:
                    </Typography>
                    <Typography id="modal-modal-description" sx={{ mb: 2 }}>
                        {'PENDING'}
                    </Typography>
                    <Typography id="modal-modal-title" variant="h6" component="h2">
                        Task ID:
                    </Typography>
                    <Typography id="modal-modal-description" sx={{ mb: 2 }}>
                        {taskId}
                    </Typography>
                </Box>
            </Modal>
            <MainCard title="Search by Variables">
                {varibleNames !== undefined && varibleNames.length !== 0 ? (
                    <Box display="grid" gridTemplateColumns="repeat(12, 1fr)" gap={4}>
                        <Box gridColumn="span 9">
                            <Stack spacing={3} marginBottom={3}>
                                <Autocomplete
                                    multiple
                                    id="tags-filled"
                                    options={varibleNames.map((option) => option)}
                                    defaultValue={[varibleNames[13]]}
                                    freeSolo
                                    disableCloseOnSelect
                                    value={selectedVariables}
                                    onChange={handleAutocompleteChange}
                                    renderTags={(value, getTagProps) =>
                                        value.map((option, index) => {
                                            const { key, ...tagProps } = getTagProps({ index });
                                            return <Chip variant="outlined" label={option} key={key} {...tagProps} />;
                                        })
                                    }
                                    renderInput={(params) => (
                                        <TextField {...params} variant="filled" label="Select columns" placeholder="columns" />
                                    )}
                                />
                            </Stack>
                            <Button variant="contained" onClick={handleGlobalVaribles}>
                                Add/Update to variables list
                            </Button>
                        </Box>

                        <Box gridColumn="span 3">
                            <VariableList />
                        </Box>
                    </Box>
                ) : (
                    <LinearProgress />
                )}
            </MainCard>
        </>
    );
};

export default SearchByVaribles;
